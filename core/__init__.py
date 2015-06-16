import core.managers.user_manager
import core.managers.stock_manager
import core.models.base as base


base.managers.register(
    'prod',
    {
        "user_manager": core.managers.user_manager.UserManager,
        "stock_manager": core.managers.stock_manager.StockManager,
    }
)
base.managers.set_group('prod')
