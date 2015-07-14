var React = require('react');
var moment = require('moment');

var Utils = {

  formatResult: function(val) {
    if (val && val.value) {
      return val.value + ' ' + (val.units || '');
    }
    return val;
  },

  timeDeltaHtml: function(strDate) {
    if (!strDate) {
      return null;
    }

    var started = moment(strDate);
    var displayDate;

    if (moment().diff(started, 'days') > 30) {
      displayDate = started.format('YYYY-MM-DD');
    }
    else {
      displayDate = started.fromNow();
    }

    return (
      <span title={strDate.replace("T", " ")}>
        {displayDate}
      </span>
    );
  }

}

module.exports = Utils;
