from __future__ import absolute_import
from __future__ import unicode_literals
from flask.ext.babel import lazy_gettext as _
from flask.ext.wtf import Form as WTSecureForm
from wtforms import (
    SelectField, TextField, validators
)
from ..models import (
    LocationType, Participant
)
from ..services import (
    locations, participants, participant_partners, participant_roles)


def _make_choices(qs, placeholder=None):
    if placeholder:
        return [['', placeholder]] + [[unicode(i[0]), i[1]] for i in list(qs)]
    else:
        return [['', '']] + [[unicode(i[0]), i[1]] for i in list(qs)]


def generate_location_edit_form(location, data=None):
    locs = LocationType.objects(deployment=location.deployment)

    class LocationEditForm(WTSecureForm):
        name = TextField('Name', validators=[validators.input_required()])
        code = TextField('Code', validators=[validators.input_required()])
        location_type = SelectField(
            _('Location type'),
            choices=_make_choices(
                locs.scalar('name', 'name'),
                _('Location type')
            ),
            validators=[validators.input_required()]
        )

    return LocationEditForm(formdata=data, **location._data)


def generate_participant_edit_form(participant, data=None):
    class ParticipantEditForm(WTSecureForm):
        participant_id = TextField(
            _('Participant ID'),
            validators=[validators.input_required()]
        )
        name = TextField(
            _('Name'),
            validators=[validators.input_required()]
        )
        gender = SelectField(
            _('Gender'),
            choices=Participant.GENDER,
            validators=[validators.input_required()]
        )
        role = SelectField(
            _('Role'),
            choices=_make_choices(
                participant_roles.find().scalar('id', 'name')
            ),
            validators=[validators.input_required()]
        )
        supervisor = SelectField(
            _('Supervisor'),
            choices=_make_choices(
                participants.find().scalar('id', 'name')
            ),
            validators=[validators.input_required()]
        )
        location = SelectField(
            _('Location'),
            choices=_make_choices(
                locations.find().scalar('id', 'name')
            ),
            validators=[validators.input_required()]
        )
        # partners are not required
        partner = SelectField(
            _('Partner'),
            choices=_make_choices(
                participant_partners.find().scalar('id', 'name')
            ),
        )

    return ParticipantEditForm(
        formdata=data,
        participant_id=participant.participant_id,
        name=participant.name,
        location=participant.location.id,
        gender=participant.gender.upper(),
        role=participant.role.id,
        partner=participant.partner.id,
        supervisor=participant.supervisor.id
    )
