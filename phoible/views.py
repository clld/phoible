from sqlalchemy.orm import joinedload

from clld.db.meta import DBSession
from clld.db.models.common import Contributor, Source


def about(req):
    return {
        'contributors': DBSession.query(Contributor).order_by(Contributor.name).options(
            joinedload(Contributor.contribution_assocs),
            joinedload(Contributor.references)),
        'sources': {k: Source.get(k) for k in 'ipa2005 hayes2009 moran2012a moranetal2012 cysouwetal2012 mccloyetal2013'.split()}
    }