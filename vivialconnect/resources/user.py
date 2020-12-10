"""
.. module:: user
   :synopsis: User module.
"""
from vivialconnect.common.util import Util
from vivialconnect.resources.resource import Resource, SubordinateResource
from vivialconnect.resources.countable import Countable


class Credential(SubordinateResource):
    def destroy(self):
        self.klass.request.delete(
            self._item_sub_resource_path(
                resource="users",
                id_=self.parent_resource.id,
                subresource=f"profile/credentials/{self.id}",
            )
        )

    def save(self):

        attributes = {"user": self._wrap_attributes(root=self._singular)}

        if self.id:
            response = self.klass.request.put(
                self._item_sub_resource_path(
                    resource="users",
                    id_=self.parent_resource.id,
                    subresource=f"profile/credentials/{self.id}",
                ),
                payload=attributes,
            )
        else:
            response = self.klass.request.post(
                self._item_sub_resource_path(
                    resource="users",
                    id_=self.parent_resource.id,
                    subresource=f"profile/credentials",
                ),
                payload=attributes,
            )
        credential_attributes = Util.remove_root(response)["credential"]
        self._update(credential_attributes)


class User(Resource, Countable):
    """Use the User resource to manage users and user passwords in the API.

    User properties

    ============= ======================
    Field         Description
    ============= ======================
    id            Unique identifier of the user object.
    date_created  Creation date (UTC) of the user in ISO 8601 format.
    date_modified Last modification date (UTC) of the user in ISO 8601 format.
    account_id    Unique identifier of the account that this user is part of.
    username      User's username for logging in to the account. *Max. length:* 128 characters.
    first_name    User's first name. *Max. length:* 128 characters.
    last_name     User's last name. *Max. length:* 128 characters.
    email         User's email address. *Max. length:* 128 characters.
    ============= ======================

    Example request to retrieve a list of users accociated with the account id 12345::

        from vivialconnect import Resource, User

        Resource.api_key = ""
        Resource.api_secret = ""
        Resource.api_account_id = "12345"

        def list_users():
            users = User.find()
            for user in users:
                print(user.id, user.first_name, user.last_name)

        list_users()

    """

    @classmethod
    def _get_object_field(cls, data, field_name):
        if "user" in data:
            pass
        return data

    def get_credentials(self, id_=None):
        """
            Returns all credentials related to an user
        """
        if id_:
            url = self._custom_path(
                id_=self.id, custom_path=f"/profile/credentials/{id_}"
            )
            response_obj = Resource._build_object(
                Util.remove_root(Resource.request.get(url))
            )
            try:
                attributes = response_obj.credential
                response = Credential(attributes, parent_resource=self)
            except AttributeError:
                response = None
            return response
        else:
            url = self._custom_path(id_=self.id, custom_path="/profile/credentials")
            response_obj = Resource._build_object(
                Util.remove_root(Resource.request.get(url))
            )
            response = response_obj.credentials

            resources = []
            for attributes in response:
                resources.append(Credential(attributes, parent_resource=self))
            return resources

    def create_credential(self, name=None):
        """
            Creates a new credential with a name, if it is provided.
        """
        credential = Credential(parent_resource=self)
        if name:
            credential.name = name
        credential.save()
        return credential

    def count_credentials(self):
        """
            Returns the numeric count of all credentials assigned to an user
        """

        url = self._custom_path(id_=self.id, custom_path="/profile/credentials/count")
        response = Resource.request.get(url)
        return int(Util.remove_root(response))
