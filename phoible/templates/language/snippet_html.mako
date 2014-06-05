<%inherit file="../snippet.mako"/>
<%namespace name="util" file="../util.mako"/>

% if request.params.get('parameter'):
    ## called for the info windows on parameter maps
    <% valuesets = h.DBSession.query(h.models.ValueSet).filter(h.models.ValueSet.parameter_pk == int(request.params['parameter'])).filter(h.models.ValueSet.language_pk == ctx.pk).all() %>
    <h3>${h.link(request, ctx)}</h3>
    % for valueset in valuesets:
        <ul>
            % for value in valueset.values:
            <li>
                Inventory ${h.link(request, valueset.contribution)}.
                % if valueset.references:
                <p>Sources: ${h.linked_references(request, valueset)}</p>
                % endif
            </li>
            % endfor
        </ul>
    % endfor
% else:
<h3>${h.link(request, ctx)}</h3>
${h.format_coordinates(ctx)}
% endif