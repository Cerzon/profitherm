$(document).ready(function(){
    if (!Modernizr.flexbox) {
        var $traveler = $('#rightsidebar').detach();
        $traveler.insertBefore('main');
        $traveler = $('#footer-right').detach();
        $traveler.insertBefore('#page-footer nav');
    }
});