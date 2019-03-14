<%inherit file="../home_comp.mako"/>
<%namespace name="util" file="../util.mako"/>


<%def name="sidebar()">
    % if ctx.url:
        <%util:well title="Online">
            ${h.external_link(ctx.url)}
        </%util:well>
    % endif
    <%util:well title="Sources">
        <ul>
            % for ref in ctx.references:
                <li>${h.link(request, ref.source, label=ref.source.description)}<br/>
                    <small>${h.link(request, ref.source)}</small>
                </li>
            % endfor
        </ul>

    </%util:well>
</%def>


<h2>Contributor ${ctx.id}: ${ctx.name}</h2>

<%util:well>
    ${u.desc(request, ctx.description)|n}
</%util:well>



<div class="tabbable">
    <ul class="nav nav-tabs">
        <li class="active"><a href="#inventories" data-toggle="tab">Inventories</a></li>
        <li><a href="#description" data-toggle="tab">Description</a></li>
    </ul>
    <div class="tab-content" style="overflow: visible;">
        <div id="inventories" class="tab-pane active">
                <%util:table args="item" items="${[a.contribution for a in ctx.contribution_assocs]}">
            <%def name="head()">
                <th>Inventory</th>
                <th>Language</th>
                <th>Segments</th>
                <th>Vowels</th>
                <th>Consonants</th>
                <th>Tones</th>
            </%def>
                <td>${h.link(request, item)}</td>
                <td>${h.link(request, item.language)}</td>
                <td>${item.count}</td>
            % for c in 'vowel consonant tone'.split():
                <td>${getattr(item, 'count_' + c)}</td>
            % endfor
            </%util:table>
        </div>
        <div id="description" class="tab-pane">
            ${u.readme(ctx.jsondata['readme'])|n}
        </div>
    </div>
    <script>
        $(document).ready(function () {
            if (location.hash !== '') {
                $('a[href="#' + location.hash.substr(2) + '"]').tab('show');
            }
            return $('a[data-toggle="tab"]').on('shown', function (e) {
                return location.hash = 't' + $(e.target).attr('href').substr(1);
            });
        });
    </script>
</div>
