<%inherit file="../home_comp.mako"/>
<%namespace name="util" file="../util.mako"/>

<%def name="sidebar()">
    <%util:well title="Cite">
        ${h.newline2br(h.text_citation(request, ctx))|n}
        ${h.cite_button(request, ctx)}
    </%util:well>
</%def>

<h2>Welcome to PHOIBLE Online</h2>

<p>The Phonetics Information Base and Lexicon (PHOIBLE) is a repository of cross-linguistic phonological inventory data, which have been extracted from source documents and tertiary databases and compiled into a single searchable convenience sample. There are currently ${inventory_count} inventories that contain ${segment_count} segment types found in ${language_count} distinct languages.</p>

<p>References are provided for each source; note that some languages in PHOIBLE have multiple entries based on distinct sources that disagree about the number and/or identity of that language’s phonemes.</p>

<p>Two principles guide the development of PHOIBLE, though it has proved challenging both theoretically and technologically to abide by them:</p>

<ol>
<li>Be faithful to the language description in the source document (now often called ‘doculect’, for reasons indicated above)</li>

<li>Encode all character data in a consistent representation in Unicode IPA</li>
</ol>

<p>In addition to phoneme inventories, PHOIBLE includes distinctive feature data for every phoneme in every language. The feature system used was created by the PHOIBLE developers to be descriptively adequate cross-linguistically. In other words, if two phonemes differ in their graphemic representation, then they necessarily differ in their featural representation as well (regardless of whether those two phonemes coexist in any known doculect). The feature system is loosely based on the feature system in
${h.link(request, hayes)} with some additions drawn from ${h.link(request, moisik)}.
##:</p>

##<p>Hayes, Bruce (2009). Introductory phonology. Oxford: Wiley-Blackwell.</p>

##<p>with some additions drawn from:</p>

##<p>Moisik, S. R., & Esling, J. H. (2011). The “whole larynx” approach to laryngeal features. In Proceedings of ICPhS 17, 1406–1409.</p>

<p>However, the final feature system goes beyond both of these sources, and is potentially subject to change as new languages are added to PHOIBLE.</p>

<p>For more information on the design, development, and challenges of PHOIBLE, see Moran 2012.</p>


<h3>How to use PHOIBLE</h3>

<p>Users can browse or search PHOIBLE's inventories by clicking on the tabs "Inventories", "Languages" or "Segments" above. Data can be downloaded by clicking the download button <insert image>. If you use PHOIBLE in your research, please cite appropriately, following our recommended citation format.</p>


<h3>How to cite PHOIBLE</h3>

<p>If you are citing the database as a whole, or making use of the phonological distinctive feature systems in PHOIBLE, please cite as follows:</p>

    <%util:well>
        ${h.newline2br(h.text_citation(request, ctx))|n}
        ${h.cite_button(request, ctx)}
    </%util:well>

<p>If you are citing phoneme inventory data for a particular language or languages, please use the name of the language as the title, and include the original data source as an element within PHOIBLE:<p>

"Lele." Data from Frajzyngier, Zygmunt (2001). A grammar of Lele. In Moran, S., McCloy, D., & Wright, R. (eds). PHOIBLE Online, vX.X. Leipzig: MPI-EvA. http://phoible.org/. Accessed on <insert date>.

<p>In cases where the original language description was part of another collection or database that was integrated into PHOIBLE, the reference is a bit more complicated.  Examples:</p>

"Abidji." Data from Chanard, Christian (2006). Systèmes Alphabétiques Des Langues Africaines. In Moran, S., McCloy, D., & Wright, R. (eds). PHOIBLE Online, vX.X. Leipzig: MPI-EvA. http://phoible.org/. Accessed on <insert date>.

"Chiricahua Apache." Data from Hoijer, Harry (1944). Chiricahua Apache. In Cornelius Osgood (ed.), Linguistic Structures of Native America. In Moran, S., McCloy, D., & Wright, R. (eds). PHOIBLE, vX.X. Leipzig: MPI-EvA. http://phoible.org/. Accessed on <insert date>.
