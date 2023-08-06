from jumpscale.packages.marketplace.chats.publisher import Publisher
from jumpscale.sals.chatflows.chatflows import chatflow_step


class WikiDeploy(Publisher):

    title = "Deploy a Wiki"
    SOLUTION_TYPE = "wiki"  # chatflow used to deploy the solution
    EXAMPLE_URL = "https://github.com/threefoldfoundation/wiki_example"

    @chatflow_step(title="Wiki Setup")
    def configuration(self):
        self.user_email = self.user_info()["email"]
        form = self.new_form()
        title = form.string_ask("Title", required=True)
        url = form.string_ask("Repository URL", required=True, is_git_url=True)
        branch = form.string_ask("Branch", required=True)
        msg = self.get_mdconfig_msg()
        form.ask(msg, md=True)
        self.envars = {
            "TYPE": "wiki",
            "NAME": "entrypoint",
            "TITLE": title.value,
            "URL": url.value,
            "BRANCH": branch.value,
            "EMAIL": self.user_email,
        }


chat = WikiDeploy
