
from datetime import datetime
from twisted.internet import defer
from buildbot.changes import base
from buildbot.util import bytes2unicode
from buildbot.util import datetime2epoch
from buildbot.util import httpclientservice
from buildbot.util.state import StateMixin


class GitHubAPI(base.ReconfigurablePollingChangeSource, StateMixin) :

    compare_attrs = ("name", "owner", "repo", "category", "project")
    db_class_name = 'GitHubAPI'

    baseurl = "api.github.com"

    def __init__(self, owner, repo, **kwargs):
        name = kwargs.get("name")
        if not name:
            kwargs["name"] = self.__class__.__name__ + ":" + owner + "/" + repo
        super(self.__class__, self).__init__(owner, repo, **kwargs)

    def checkConfig(self, owner, repo, project=None, token=None, **kwargs):
        super().checkConfig(name=self.name, **kwargs)

    @defer.inlineCallbacks
    def reconfigService(self, owner, repo, project=None, token=None, **kwargs):
        yield super().reconfigService(name=self.name, **kwargs)

        self.owner = owner
        self.repo = repo

        # Buildbot meta data
        self.category = kwargs.get("category")
        self.project = project if project else "/".join([owner, repo])

        # HTTP
        self.baseurl = kwargs.get("baseurl", self.baseurl)

        # Headers
        http_headers = {'User-Agent': 'Buildbot'}
        if token is not None:
            http_headers.update({'Authorization': 'token ' + token})

        self._http = yield httpclientservice.HTTPClientService.getService(
            self.master, "https://" + self.baseurl, headers=http_headers, debug=True)

    def describe(self):
        return ("{} watching the GitHub repository {}/{}").format(self.__class__.__name__, self.owner, self.repo)

    def getApiUri(self, owner, repo, resource=None) :
        uri = "/repos/{0}/{1}".format(owner, repo)
        if resource :
            uri += '/' + resource
        return uri

    @defer.inlineCallbacks
    def poll(self) :
        yield self._getReleases()

    @defer.inlineCallbacks
    def _cache(self, id, type="release") :
        state = self.master.db.state
        cache_id = '%s-%d' % (type, id)
        object_id = yield state.getObjectId('{}/{}'.format(self.owner, self.repo), self.db_class_name)

        hit = yield state.getState(object_id, cache_id, False)
        if not hit :
            # Update state on miss.
            yield state.setState(object_id, cache_id, True)
        return hit

    def _getFiles(self, files) :
        return [f["filename"] for f in files]

    @defer.inlineCallbacks
    def _getUser(self, id) :
        result = yield self._http.get("/users/" + id)
        data = yield result.json()
        return data

    @defer.inlineCallbacks
    def _getCommit(self, ref) :
        url = "/".join([self.getApiUri(self.owner, self.repo, "commits"), ref])
        result = yield self._http.get(url)
        data = yield result.json()
        return data

    @defer.inlineCallbacks
    def _processRelease(self, release) :
        tag = release["tag_name"]
        name = release["name"]
        body = release["body"]
        branch = release["target_commitish"]

        commit_data = yield self._getCommit(tag)
        user_data = yield self._getUser(release["author"]["login"])

        author_name = user_data["name"]
        committer = commit_data["commit"]["committer"]

        timestamp = None
        for field in ['updated_at', 'published_at'] :
            if field in release :
                timestamp = datetime.strptime(release[field], '%Y-%m-%dT%H:%M:%SZ')
                break

        properties = {
            "sha" : commit_data["sha"],
            "id" : release["id"],
        }

        yield self.master.data.updates.addChange(
                author=author_name,
                committer="{0} <{1}>".format(committer["name"], committer["email"]),
                revision=tag,
                files=self._getFiles(commit_data["files"]),
                comments="\r\n\r\n".join(["#{} - {}".format(release["id"], name), body]),
                when_timestamp=datetime2epoch(timestamp),
                branch=branch,
                project=self.project,
                repository=bytes2unicode("https://github.com/{0}/{1}.git".format(self.owner, self.repo), encoding="UTF-8"),
                category=self.category,
                properties=properties,
                src='git')

    @defer.inlineCallbacks
    def _getReleases(self):
        result = yield self._http.get(self.getApiUri(self.owner, self.repo, "releases"))
        releases = yield result.json()
        for release in releases :
            # Process release if it did not exist in cache.
            if not (yield self._cache(release["id"])) :
                yield self._processRelease(release)
