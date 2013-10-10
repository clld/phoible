<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">Segment ${ctx.name}</%block>

##<%def name="sidebar()">
    ##<%util:well title="Properties">
    ##    <dl>
    ##        <dt>Segment class</dt>
    ##        <dd>${ctx.segment_class}</dd>
    ##        <dt>Combined class</dt>
    ##        <dd>${ctx.combined_class}</dd>
    ##    </dl>
    ##</%util:well>
    ##<%util:well title="Features">
    ##    <table class="table table-condensed">
    ##    % for value in ctx.phoneme.unitvalues:
    ##        <tr>
    ##            <td>${h.link(request, value.unitparameter)}</td>
    ##            <td>${h.link(request, value)}</td>
    ##        </tr>
    ##    % endfor
    ##    </table>
    ##</%util:well>
##</%def>


<h2>Segment ${ctx.name}</h2>
<div style="width: 20%;">
${util.dl_table(('Segment class', ctx.segment_class), ('Combined class', ctx.combined_class))}
</div>

% if request.map:
${request.map.render()}
% endif

<div>
    <% dt = request.registry.getUtility(h.interfaces.IDataTable, 'values'); dt = dt(request, h.models.Value, parameter=ctx) %>
    ${dt.render()}
</div>
