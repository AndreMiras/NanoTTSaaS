/**
 * Binds the Text To Speak form submit event
 * with AJAX post and plays sound.
 */
function bind_tts_form(api_url)
{
  var form_id = "#ttsForm";
  // this is the id of the form
  $(form_id).submit(function(e) {
    // plays a short silent sound just after a gesture
    // to work around Android protection
    play_empty();
    $.ajax({
      type: "POST",
      url: api_url,
      // serializes the form's elements.
      data: $(form_id).serialize(),
      success: function(data)
      {
        var audio_file = data.audio_file;
        play_sound(audio_file);
      }
    });
    
    // avoid to execute the actual submit of the form.
    e.preventDefault();
  });
}

function play_sound(file_url)
{
  var mySoundObject = soundManager.createSound({
    url: file_url
  });
  mySoundObject.play();
}

/**
 * Plays a short silent sound to Work arounds Android protection
 * http://stackoverflow.com/a/32571967/185510
 */
function play_empty()
{
  var file_url = "/static/empty.wav";
  play_sound(file_url);
}
