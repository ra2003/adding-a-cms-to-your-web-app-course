from typing import Optional

from pypi_org.data.redirects import Redirect
from pypi_org.infrastructure.num_convert import try_int
from pypi_org.services import cms_service
from pypi_org.viewmodels.shared.viewmodelbase import ViewModelBase


class EditRedirectViewModel(ViewModelBase):
    def __init__(self, redirect_id: Optional[str] = None):
        super().__init__()

        self.name = ''
        self.url = ''
        self.short_url = self.request_dict.get('short_url', '')
        self.redirect_id: Optional[int] = try_int(redirect_id)
        self.redirect: Optional[Redirect] = None

        if self.redirect_id:
            self.redirect = cms_service.get_redirect_by_id(self.redirect_id)
            if not self.redirect:
                self.error = f"A redirect with id {self.redirect_id} does not exists."
                return

            self.name = self.redirect.name
            self.url = self.redirect.url
            self.short_url = self.redirect.short_url

    def restore_from_dict(self):
        self.name = self.request_dict.get('name', self.name)
        self.url = self.request_dict.get('url', self.url)
        self.short_url = self.request_dict.get('short_url')

        if not self.redirect_id:
            redirect = cms_service.get_redirect(self.short_url)
            if redirect:
                self.error = f"A redirect with URL {self.short_url} already exists."
                return
