jQuery(function($) {
  var reasons = [];
  var submitConsentForm = function(evt) {
    var form = $(this).closest('form');
    var data = form.serialize();
    var url = form.attr('action');
    data += '&'+this.name+'=1';
    $.ajax({
      type: "POST",
      url: url,
      data: data,
    }).done(function() {
      setConsentForm();
    });
    evt.preventDefault();
  };
  var setConsentForm = function() {
    if (reasons.length > 0) {
      $('#gdpr-consent-banner').show();
      var reason = reasons.shift();
      $('#gdpr-consent-banner form .gdpr-reason').html(
        '<strong>' + reason.Title + '</strong>' +
        '<p>' + reason.Description + '</p>' +
        '<input type="hidden" name="processing_reason" value="' + reason.name + '" />'
      );
      $('#gdpr-consent-banner form .gdpr-actions input').one('click', submitConsentForm);
    } else {
      $('#gdpr-consent-banner').remove();
    }
  };
  var url = $('#gdpr-consent-banner form').data('json-url');
  $.ajax({
    type: "GET",
    url: url,
    headers: {"Cache-Control": "no-cache"},
  }).done(function(data) {
    reasons = data;
    setConsentForm();
  });
});
