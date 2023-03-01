# flake8: noqa
from flaskr import db

from .tables import (
    composer_performer, composer_style,
    performer_style, composer_title,
    performer_title, performer_contemporaries,
    composer_contemporaries, composer_favorites,
    performer_favorites, composer_nationalities,
    performer_nationalities
)
from .composer import Composer
from .performer import Performer
from .style import Style
from .recording import Recording
from .period import Period
from .composition import Composition
from .recording import Recording
from .title import Title
from .nation import Nation
from .user import User