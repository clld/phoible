## -*- coding: utf-8 -*-
<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="ipa" file="../ipa.mako"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>
<% ia = [ref.source for ref in ctx.references if ref.source.jsondatadict.get('internetarchive_id')] %>
<% if ia: ia = ia[0].jsondatadict['internetarchive_id'] %>

<%block name="head">
    <link type="text/css" rel="stylesheet" href="${request.static_url('phoible:static/ipa.css')}"/>
</%block>

<h2>
    ${_('Contribution')} ${ctx.name}
    % if ctx.source_url:
        ${h.external_link(ctx.source_url, label=' ', title=ctx.source_url)}
    % endif
</h2>

% if ctx.description:
    <p>
        Source name: <i>${ctx.description}</i>
    </p>
% endif

<div class="tabbable">
    <ul class="nav nav-tabs">
        <li class="active"><a href="#segments" data-toggle="tab">Segment list</a></li>
        <li><a href="#ipa" data-toggle="tab">IPA chart</a></li>
        % if ctx.internetarchive_url or ia:
        <li><a href="#source" data-toggle="tab">Source</a></li>
        % endif
    </ul>
    <div class="tab-content" style="overflow: visible;">
        <div id="segments" class="tab-pane active">
            ${request.get_datatable('values', h.models.Value, contribution=ctx).render()}
        </div>
        <div id="ipa" class="tab-pane">
            ${ipa.chart({vs.parameter.name: vs.parameter for vs in ctx.valuesets}, u.segment_link)}
        </div>
        % if ctx.internetarchive_url or ia:
        <div id="source" class="tab-pane">
            % if ctx.internetarchive_url:
                <iframe src='https://archive.org/stream/${ctx.internetarchive_url.split('/')[-1]}?ui=embed#mode/1up' width='680px' height='750px' frameborder='1' ></iframe>
            % else:
                <iframe src='https://archive.org/stream/${ia}?ui=embed#mode/1up' width='680px' height='750px' frameborder='1' ></iframe>
            % endif
        </div>
        % endif
    </div>
    <script>
$(document).ready(function() {
    if (location.hash !== '') {
        $('a[href="#' + location.hash.substr(2) + '"]').tab('show');
    }
    return $('a[data-toggle="tab"]').on('shown', function(e) {
        return location.hash = 't' + $(e.target).attr('href').substr(1);
    });
});
    </script>
</div>

<%def name="sidebar()">
    <%util:well title="Contributor">
        ${h.linked_contributors(request, ctx)}
        ${h.cite_button(request, ctx)}
    </%util:well>
    <%util:well title="Sources">
        ${util.stacked_links(ref.source for ref in ctx.references)}
    </%util:well>
    <%util:well>
        <h3>${h.link(request, ctx.language)}</h3>
        ${util.language_meta(lang=ctx.language)}
    </%util:well>
</%def>
