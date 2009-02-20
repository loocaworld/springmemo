import oauth
import httplib
#from etree import ElementTree
#from xml import etree
import xml.etree.ElementTree as ET

class SpringnoteClient:

    SPRINGNOTE_PROTOCOL = 'http'
    SPRINGNOTE_SERVER = 'api.springnote.com'
    SPRINGNOTE_PORT = 80
    
    REQUEST_TOKEN_URL = 'https://api.springnote.com/oauth/request_token'
    ACCESS_TOKEN_URL = 'https://api.springnote.com/oauth/access_token'
    AUTHORIZATION_URL = 'https://api.springnote.com/oauth/authorize'
    
    def __init__(self, consumer_token, consumer_token_secret):
        self.consumer = oauth.OAuthConsumer(consumer_token, consumer_token_secret)
        self.signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
        
    def create_oauth_request_for_request_token(self):
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, http_url=self.REQUEST_TOKEN_URL)
        oauth_request.sign_request(oauth.OAuthSignatureMethod_HMAC_SHA1(), self.consumer, None)
        return oauth_request
        
    def fetch_request_token(self):
        oauth_request = self.create_oauth_request_for_request_token()
                
        connection = httplib.HTTPSConnection("%s:%d" % ('api.springnote.com', 443))
        connection.request(oauth_request.http_method, self.REQUEST_TOKEN_URL, headers=oauth_request.to_header()) 
        response = connection.getresponse()
        body = response.read()
        if body.startswith('Invalid OAuth Request'):
            raise SpringnoteError.NotAuthorized
        return oauth.OAuthToken.from_string(body)
    
    def create_oauth_request_for_access_token(self, token):
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, token=token, http_url=self.ACCESS_TOKEN_URL)
        oauth_request.sign_request(oauth.OAuthSignatureMethod_HMAC_SHA1(), self.consumer, token)
        return oauth_request
        
    def fetch_access_token(self):
        oauth_request = self.create_oauth_request_for_request_token()
                
        connection = httplib.HTTPSConnection("%s:%d" % ('api.springnote.com', 443))
        connection.request(oauth_request.http_method, self.ACCESS_TOKEN_URL, headers=oauth_request.to_header()) 
        response = connection.getresponse()
        body = response.read()
        if body.startswith('Invalid OAuth Request'):
            raise SpringnoteError.NotAuthorized
        
        self.access_token = oauth.OAuthToken.from_string(body)
        return self.access_token
    
    # todo
    def get_page(self, id, domain=None):
        url = "%s://%s/pages/%d.xml" % (self.SPRINGNOTE_PROTOCOL, self.SPRINGNOTE_SERVER, id)
        parameters = {}
        if domain:
            parameters['domain'] = domain
            url += "?domain=%s" % domain
        
        print url
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, token=self.access_token, http_method='GET', http_url=url, parameters=parameters)
        oauth_request.sign_request(self.signature_method, self.consumer, self.access_token)        

        connection = httplib.HTTPConnection("%s:%d" % (self.SPRINGNOTE_SERVER, self.SPRINGNOTE_PORT))
        connection.request('GET', url, headers=oauth_request.to_header())
        response = connection.getresponse()
        body = response.read()
        print "----body----"
        print body
        print "------------"
        return Page(body)

class SpringnoteError:
    class NotAuthorized(RuntimeError):
        pass

class Page:
    def __init__(self, xml=None):
        #self.identifier = None
        #self.date_created = None
        #self.date_modified = None
        #self.rights = None
        #self.creator = None
        #self.contributor_modified = None
        if(xml != None):
            self.parse_xml(xml)

        
    def parse_xml(self,xml):
        tree = ET.XML(xml)
        self.identifier =  tree[0].text
        self.date_created = tree[5].text
        self.date_modified = tree[3].text
        self.rights = tree[7].text
        self.creator = tree[8].text
        self.contributor_modified = tree[9].text
        self.title = tree[1].text
        self.source = tree[6].text
        self.relation_is_part_of = tree[2].text
        self.uri = tree[4].text
#        self.identifier =  tree.find('identifier').text
#        self.date_created = tree.find('date_created').text
#        self.date_modified = tree.find('date_modified').text
#        self.rights = tree.find('rights').text
#        self.creator = tree.find('creator').text
#        self.contributor_modified = tree.find('contributor_modified').text
#        self.title = tree.find('title').text
#        self.source = tree.find('source').text
#        self.relation_is_part_of = tree.find('relation_is_part_of').text
#        self.uri = tree.find('uri').text

    def to_s(self):
        return "%s %s %s %s %s %s" % (self.identifier,self.date_created,
                self.date_modified, self.rights,
                self.creator, self.contributor_modified)

