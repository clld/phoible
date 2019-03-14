## -*- coding: utf-8 -*-
<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">${ctx.segment_class.capitalize()} ${ctx.name}</%block>

<%block name="head">
    <link href="${request.static_url('clld:web/static/css/charissil.css')}" rel="stylesheet">
</%block>

<%def name="sidebar()">
    <%util:well title="Features">
        <table class="table table-condensed">
        % for d in ctx.data:
            <tr>
                <td>${d.key}</td>
                <td>${d.value}</td>
            </tr>
        % endfor
        </table>
    </%util:well>
</%def>

<div style="float: right; margin-top: 10px;">
    ${h.alt_representations(request, ctx, doc_position='left', exclude=['md.html'])}
</div>

<h2>
    ${ctx.segment_class.capitalize()} <span class="charissil">${ctx.name}</span>
    % if ctx.jsondata.get('wikipedia_url'):
        <a href="${ctx.jsondata['wikipedia_url']}"
           title="go to related article on wikipedia">
            <img src="${request.static_url('phoible:static/wikipedia_32.png')}"/>
        </a>
    % endif
</h2>
<p class="alert alert-info">
    ${ctx.description}
</p>

% if request.map:
${request.map.render()}
% endif

${request.get_datatable('values', h.models.Value, parameter=ctx).render()}
