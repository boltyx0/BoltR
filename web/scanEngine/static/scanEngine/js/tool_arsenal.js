function get_external_tool_latest_version(tool_id, tool_name){
  var current_version = document.getElementById(tool_name+'_current').textContent;
  console.log(current_version)
  if (current_version === 'Invalid version lookup command.' || current_version === 'Version Lookup command not provided.'){
    Swal.fire({
      title: 'Unable to fetch latest version!',
      text: `Since the version lookup command is invalid, BoltR is not able to detect if there's a newer version. But you can still force download the latest version.`,
      icon: 'info',
      confirmButtonText: 'Update ' +  htmlEncode(tool_name)
    }).then((result) => {
      /* Read more about isConfirmed, isDenied below */
      if (result.isConfirmed) {
        Swal.fire({
          title: 'Downloading latest version...',
          text: 'This may take a few minutes.',
          allowOutsideClick: false
        });
        swal.showLoading();
        fetch('/api/tool/update/?tool_id=' + tool_id, { credentials: 'same-origin' })
        .then(function (response) {
          return response.json().then(function (data) {
            return { ok: response.ok, data: data };
          });
        })
        .then(function (result) {
          swal.close();
          if (result.ok && result.data['status']) {
            Swal.fire({
              title:  htmlEncode(tool_name) + ' update started',
              text: result.data['message'] || 'Running in background. This may take a few minutes.',
              icon: 'success',
            });
          } else {
            Swal.fire({
              title:  htmlEncode(tool_name) + ' could not update',
              text: (result.data && result.data['message']) || 'Request failed.',
              icon: 'error',
            });
          }
        })
        .catch(function (err) {
          swal.close();
          Swal.fire({
            title: 'Update failed',
            text: 'Request failed or timed out. The update may still be running in the background.',
            icon: 'error',
          });
        });
      }
    });
  }
  else{
    Swal.fire({
      title: 'Finding latest version...',
      allowOutsideClick: false
    });
    swal.showLoading();
    fetch('/api/github/tool/get_latest_releases/?tool_id=' + tool_id, { credentials: 'same-origin' })
    .then(response => response.json())
    .then(function (response) {
      swal.close();
      if (response['message'] == 'RateLimited') {
        Swal.fire({
          showCancelButton: true,
          title: 'Error!',
          text: 'Github API rate limit exceeded, we can not fetch the latest version number, please try again in an hour. But you can force download the latest version.',
          icon: 'error',
          confirmButtonText: 'Force download',
        }).then((result) => {
          if (result.isConfirmed) {
            Swal.fire({
              title: 'Downloading latest version...',
              text: 'This may take a few minutes.',
              allowOutsideClick: false
            });
            swal.showLoading();
            fetch('/api/tool/update/?tool_id=' + tool_id, { credentials: 'same-origin' })
            .then(function (res) { return res.json().then(function (data) { return { ok: res.ok, data: data }; }); })
            .then(function (r) {
              swal.close();
              if (r.ok && r.data['status']) {
                Swal.fire({ title: htmlEncode(tool_name) + ' update started', text: r.data['message'] || 'Running in background.', icon: 'success' });
              } else {
                Swal.fire({ title: htmlEncode(tool_name) + ' could not update', text: (r.data && r.data['message']) || 'Request failed.', icon: 'error' });
              }
            })
            .catch(function () { swal.close(); Swal.fire({ title: 'Update failed', text: 'Request failed or timed out.', icon: 'error' }); });
          }
        });;
      }
      else if (response['message'] == 'Tool Not found'){
        Swal.fire({
          title: 'Oops!',
          text: 'We ran into an error! Please raise github request.',
          icon: 'error'
        });
      }
      else if (response['message'] == 'Not Found'){
        Swal.fire({
          showCancelButton: true,
          title: 'Oops!',
          text: 'The github URL provided is not valid, or the project doesn\'t support releases. We are unable to check the latest version number, however, you can still force download the update',
          icon: 'error',
          confirmButtonText: 'Force download',
        }).then((result) => {
          /* Read more about isConfirmed, isDenied below */
          if (result.isConfirmed) {
            Swal.fire({
              title: 'Downloading latest version...',
              text: 'This may take a few minutes.',
              allowOutsideClick: false
            });
            swal.showLoading();
            fetch('/api/tool/update/?tool_id=' + tool_id, { credentials: 'same-origin' })
            .then(function (res) { return res.json().then(function (data) { return { ok: res.ok, data: data }; }); })
            .then(function (r) {
              swal.close();
              if (r.ok && r.data['status']) {
                Swal.fire({ title: htmlEncode(tool_name) + ' update started', text: r.data['message'] || 'Running in background.', icon: 'success' });
              } else {
                Swal.fire({ title: htmlEncode(tool_name) + ' could not update', text: (r.data && r.data['message']) || 'Request failed.', icon: 'error' });
              }
            })
            .catch(function () { swal.close(); Swal.fire({ title: 'Update failed', text: 'Request failed or timed out.', icon: 'error' }); });
          }
        });;
      }
      else{
        // match current version with installed version
        // sometimes version names can be v1.1.1 or 1.1.1, so for consistency
        // let's remove v from both
        var latest_version = response['name'];
        latest_version = latest_version.charAt(0) == 'v' ? latest_version.substring(1) : latest_version;

        if (current_version === 'Invalid version lookup command.' || current_version === 'Version Lookup command not provided.'){
          Swal.fire({
            title: 'Unable to fetch latest version!',
            text: `Since the version lookup command is invalid, BoltR is not able to detect if there's a newer version. But you can still force download the latest version. The latest version is ${latest_version}.`,
            icon: 'info',
            confirmButtonText: 'Update ' +  htmlEncode(tool_name)
          }).then((result) => {
            /* Read more about isConfirmed, isDenied below */
            if (result.isConfirmed) {
              Swal.fire({
                title: 'Downloading latest version...',
                text: 'This may take a few minutes.',
                allowOutsideClick: false
              });
              swal.showLoading();
              fetch('/api/tool/update/?tool_id=' + tool_id, { credentials: 'same-origin' })
              .then(function (res) { return res.json().then(function (data) { return { ok: res.ok, data: data }; }); })
              .then(function (r) {
                swal.close();
                if (r.ok && r.data['status']) {
                  Swal.fire({ title: htmlEncode(tool_name) + ' update started', text: r.data['message'] || 'Running in background. This may take a few minutes.', icon: 'success' });
                } else {
                  Swal.fire({ title: htmlEncode(tool_name) + ' could not update', text: (r.data && r.data['message']) || 'Request failed.', icon: 'error' });
                }
              })
              .catch(function () { swal.close(); Swal.fire({ title: 'Update failed', text: 'Request failed or timed out.', icon: 'error' }); });
            }
          });
        }
        else{
          current_version = current_version.charAt(0) == 'v' ? current_version.substring(1) : current_version;
          if (current_version == latest_version) {
            Swal.fire({
              title: 'No Update available',
              text: 'Looks like the latest version of ' +  htmlEncode(tool_name) + ' is already installed.',
              icon: 'info'
            });
          }
          else{
            // update available
            Swal.fire({
              title: 'Update available! Version: ' + latest_version,
              text: `Your current version of ${ htmlEncode(tool_name)} is v${current_version}, but latest version v${latest_version} is available, please update!`,
              icon: 'info',
              confirmButtonText: 'Update ' +  htmlEncode(tool_name)
            }).then((result) => {
              if (result.isConfirmed) {
                Swal.fire({
                  title: 'Downloading latest version...',
                  text: 'This may take a few minutes.',
                  allowOutsideClick: false
                });
                swal.showLoading();
                fetch('/api/tool/update/?tool_id=' + tool_id, { credentials: 'same-origin' })
                .then(function (res) { return res.json().then(function (data) { return { ok: res.ok, data: data }; }); })
                .then(function (r) {
                  swal.close();
                  if (r.ok && r.data['status']) {
                    Swal.fire({ title: htmlEncode(tool_name) + ' update started', text: r.data['message'] || 'Running in background. This may take a few minutes.', icon: 'success' });
                  } else {
                    Swal.fire({ title: htmlEncode(tool_name) + ' could not update', text: (r.data && r.data['message']) || 'Request failed.', icon: 'error' });
                  }
                })
                .catch(function () { swal.close(); Swal.fire({ title: 'Update failed', text: 'Request failed or timed out.', icon: 'error' }); });
              }
            });
          }
        }
      }
    });
  }
}

function get_external_tool_current_version(tool_id, id){
  fetch('/api/external/tool/get_current_release/?tool_id=' + tool_id, { credentials: 'same-origin' })
  .then(response => response.json())
  .then(function (response){
    if (response['status']){
      version_number = response['version_number'].charAt(0) == 'v' || response['version_number'].charAt(0) == 'V' ? response['version_number'] : 'v' + response['version_number'];
      document.getElementById(id).innerHTML = '<span class="badge badge-soft-primary">' + version_number + '</span>';
    }
    else{
      document.getElementById(id).innerHTML = '<span class="badge badge-soft-danger">' + response['message'] + '</span>';
    }
  });
}

function uninstall_tool(tool_id, tool_name){
  Swal.fire({
    title: 'Are you sure you want to uninstall ' + htmlEncode(tool_name),
    text: `This is not reversible. Please proceed with caution.`,
    icon: 'warning',
    confirmButtonText: 'Uninstall ' +  htmlEncode(tool_name)
  }).then((result) => {
    /* Read more about isConfirmed, isDenied below */
    if (result.isConfirmed) {
      Swal.fire({
        title: 'Uninstalling ' + htmlEncode(tool_name),
        text: 'This may take a few minutes...',
        allowOutsideClick: false
      });
      swal.showLoading();
      fetch('/api/tool/uninstall/?tool_id=' + tool_id, { credentials: 'same-origin' })
      .then(response => response.json())
      .then(function (response) {
        console.log(response);
        swal.close();
        $("#tool_card_" + tool_name).remove();
        Swal.fire({
          title:  htmlEncode(tool_name) + ' Uninstalled!',
          text: `${tool_name} has been Uninstalled.`,
          icon: 'success',
        });
      });
    }
  });
}


// show hide tools
$('#btn_show_custom_tools').on('click', function () {
  $('.custom_tool').show();
  $('.default_tool').hide();
  Snackbar.show({
    text: 'Filtered custom tools',
    pos: 'top-right',
    duration: 2500
  });
  $('#btn_show_custom_tools').addClass('btn-primary').removeClass('btn-light');
  $('#btn_show_all_tools').addClass('btn-light');
  $('#btn_show_default_tools').addClass('btn-light');
});

$('#btn_show_default_tools').on('click', function () {
  $('.custom_tool').hide();
  $('.default_tool').show();
  Snackbar.show({
    text: 'Filtered default tools',
    pos: 'top-right',
    duration: 2500
  });
  $('#btn_show_default_tools').addClass('btn-primary').removeClass('btn-light');
  $('#btn_show_custom_tools').addClass('btn-light');
  $('#btn_show_all_tools').addClass('btn-light');
});

$('#btn_show_all_tools').on('click', function () {
  $('.custom_tool').show();
  $('.default_tool').show();
  Snackbar.show({
    text: 'Displaying all tools',
    pos: 'top-right',
    duration: 2500
  });
  $('#btn_show_all_tools').addClass('btn-primary').removeClass('btn-light');
  $('#btn_show_custom_tools').addClass('btn-light');
  $('#btn_show_default_tools').addClass('btn-light');
});

// Wire "Check for update" button to existing update flow
$(document).on('click', '.btn-check-update', function () {
  var toolId = $(this).data('tool-id');
  var toolName = $(this).data('tool-name');
  if (toolId && toolName) {
    get_external_tool_latest_version(toolId, toolName);
  }
});

// Helper: parse JSON or return safe object so we never throw on .json()
function parseUpdateResponse(res) {
  return res.text().then(function (text) {
    var data = { message: 'No response body' };
    try {
      if (text) data = JSON.parse(text);
    } catch (e) {
      data = { message: 'Server returned non-JSON (status ' + res.status + '). Check console.' };
    }
    return { ok: res.ok, status: res.status, data: data };
  });
}

// Wire "Update to latest" button - direct update without version check
$(document).on('click', '.btn-update-now', function () {
  var toolId = $(this).data('tool-id');
  var toolName = $(this).data('tool-name');
  if (!toolId || !toolName) return;
  Swal.fire({
    title: 'Update ' + htmlEncode(toolName) + ' to latest?',
    text: 'This will run the update command in the background. It may take a few minutes.',
    icon: 'question',
    showCancelButton: true,
    confirmButtonText: 'Update'
  }).then(function (result) {
    if (!result.isConfirmed) return;
    Swal.fire({ title: 'Updating...', text: 'Running in background.', allowOutsideClick: false });
    swal.showLoading();
    var url = (window.location.origin || '') + '/api/tool/update/?tool_id=' + toolId;
    fetch(url, { credentials: 'same-origin', method: 'GET' })
      .then(parseUpdateResponse)
      .then(function (r) {
        swal.close();
        if (r.ok && r.data && r.data['status']) {
          Swal.fire({ title: htmlEncode(toolName) + ' update started', text: r.data['message'] || 'Check back in a few minutes.', icon: 'success' });
          get_external_tool_current_version(toolId, toolName + '_current');
        } else {
          Swal.fire({ title: 'Update failed', text: (r.data && r.data['message']) || 'Status ' + r.status, icon: 'error' });
        }
      })
      .catch(function (err) {
        swal.close();
        Swal.fire({ title: 'Update failed', text: 'Network error or timeout. Try again.', icon: 'error' });
      });
  });
});
