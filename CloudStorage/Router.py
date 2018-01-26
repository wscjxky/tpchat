import View.CloudStorgeView
import View.DomainView
import View.Platform
import View.WeixingDelegate


def config(app, api):
    View.CloudStorgeView.route_config(app, api)
    View.DomainView.route_config(app, api)
    View.Platform.route_config(app,api)
    View.WeixingDelegate.route_config(app, api)


