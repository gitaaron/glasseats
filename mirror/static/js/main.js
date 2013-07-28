var g_data;
$(function() {

var auth = { 
  //
  // Update with your auth tokens.
  //
  consumerKey: "dU2R4gR_UzIDuIiOg0ue9w", 
  consumerSecret: "kwpJ2uOUzm9r-aVI1NlQwN4cd9I",
  accessToken: "F0TCvDD9-bwnDwqO2qMUHXOtd9YzCNty",
  // This example is a proof of concept, for how to use the Yelp v2 API with javascript.
  // You wouldn't actually want to expose your access token secret like this in a real application.
  accessTokenSecret: "PY0NIPzKyBeU4Y1aM4qMVR8GgcY",
  serviceProvider: { 
    signatureMethod: "HMAC-SHA1"
  }
};

var terms = 'food';
var lat = '43.650252,-79.370388';

//var lat = '37.782112,-122.418648'; // SF

var accessor = {
  consumerSecret: auth.consumerSecret,
  tokenSecret: auth.accessTokenSecret
};

parameters = [];
parameters.push(['term', terms]);
//parameters.push(['location', near]);

parameters.push(['radius', 25]);
parameters.push(['callback', 'cb']);
parameters.push(['oauth_consumer_key', auth.consumerKey]);
parameters.push(['oauth_consumer_secret', auth.consumerSecret]);
parameters.push(['oauth_token', auth.accessToken]);
parameters.push(['oauth_signature_method', 'HMAC-SHA1']);

    $('#basicMessage').submit(function() {

        var ll = $('#lat').val()+','+$('#long').val();
        parameters.push(['ll', ll]);
        var message = { 
          'action': 'http://api.yelp.com/v2/search',
          'method': 'GET',
          'parameters': parameters 
        };


        OAuth.setTimestampAndNonce(message);
        OAuth.SignatureMethod.sign(message, accessor);
        var parameterMap = OAuth.getParameterMap(message.parameters);
        parameterMap.oauth_signature = OAuth.percentEncode(parameterMap.oauth_signature)
        console.log(parameterMap);

        $.ajax({
          'url': message.action,
          'data': parameterMap,
          'cache': true,
          'dataType': 'jsonp',
          'jsonpCallback': 'cb',
          'success': function(data, textStats, XMLHttpRequest) {
            g_data = data;
            console.log(data);
            var b = g_data.businesses[0];
            $.ajax({
                url:'/',
                type:'POST',
                data:{
                    operation:'insertItem',
                    message:'<article>\n  <figure>\n<img src=\"'+b.image_url+'\">\n</figure>\n  <section>\n <h1 class=\"text-large\">'+b.name+'</h1>\n    <p class=\"text-x-small\">\n      <img src=\"'+b.rating_img_url+'\">\n</p>\n <hr>\n <p class=\"text-normal\">\11:15 2:10 4:15<br>\n</p>\n</section>\n</article>\n',
                    //imageUrl:'http://s3-media1.ak.yelpcdn.com/bphoto/HpqneefkZQzErYdGAq9wmw/l.jpg'
                    //html:'<h1>'+b.name+'</h1><img src="'+b.image_ur+'" /><img src="'+b.rating_img_url+'" />'
                    html:'on'
                },
                success:function() { alert('Your message was succesfully sent to timeline.'); },
                error:function() { alert('There was a problem sending your message to the timeline.'); }
            });
          }
        });




        return false;
    });
});
