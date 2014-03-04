<%inherit file="/base/base_panels.mako"/>
<%namespace name="mod_masthead" file="/webapps/galaxy/galaxy.masthead.mako"/>

## Default title
<%def name="title()">Galaxy</%def>

<%def name="javascripts()">
${parent.javascripts()}
</%def>

<%def name="late_javascripts()">
${parent.late_javascripts()}
</%def>

## Masthead
<%def name="masthead()">
    <%
        mod_masthead.load(self.active_view);
    %>

    ## Logo, layered over tabs to be clickable
    <div class="title">
        <a href="${h.url_for( app.config.get( 'logo_url', '/' ) )}">
        <img border="0" src="${h.url_for('/static/images/galaxyIcon_noText.png')}">
        Galaxy
        </a>
        %if app.config.brand:
             / 
            <a href="${h.url_for( app.config.get( 'hcsvlab_url', '/' ) )}">
                <span>${app.config.brand}</span>
            </a>
        %endif

    </div>

</%def>