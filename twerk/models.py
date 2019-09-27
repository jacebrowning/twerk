from datafiles import datafile


@datafile("../data/users/{self.username}.yml")
class User:
    username: str

    @classmethod
    def from_url(cls, browser):
        browser.visit("https://twitter.com/home")
        browser.find_by_css('[aria-label="Profile"]').click()
        url = browser.url
        username = url.split('/')[-1]
        return cls(username)
