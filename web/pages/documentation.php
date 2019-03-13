<div class="container-fluid" style="margin-top:90px">
<h1 class="display-6"> Little Tutorial</h1>	
<p class="text-justify">In this guide we will understand how to create a profile for our backup. The profile can be used whenever we need to make a backup.</p>
<h2 class="mt-5">Make a profile</h2>
<p class="text-justify">First you need to create a profile for backup. To do this select from <kbd>File</kbd> menu: <kbd>New Profile</kbd></p>
<p class="text-justify">At this point you will need to fill in the mandatory fields with your values.<p class="text-justify">
<img src="imgs/pobkup-settings.png" class="img-fluid" alt="Settings">
<h2 class="mt-5">Required fields</h2>
<p class="text-justify">The mandatory fields are only 3: <kbd>Label</kbd>,<kbd>Source</kbd>,<kbd>Destination</kbd>  </p>
<table class="table">
  <thead>
    <tr>
      <th scope="col">Field</th>
      <th scope="col">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row"><kbd>Label</kbd></th>
      <td>A label for your backup</td>
    </tr>
    <tr>
      <th scope="row"><kbd>Source</kbd></th>
      <td>the source folder where the data is stored</td>
    </tr>
    <tr>
      <th scope="row"><kbd>Destination</kbd></th>
      <td>the folder where the data will be secured</td>
    </tr>
  </tbody>
</table>

<h2 class="mt-5">Optional fields</h2>
<table class="table">
  <thead>
    <tr>
      <th scope="col">Field</th>
      <th scope="col">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row"><kbd>Delete file from destination</kbd></th>
      <td>if you delete a file in the source folder it will also be deleted in the destination folder</td>
    </tr>
    <tr>
      <th scope="row"><kbd>History</kbd></th>
      <td>will create a folder with the date containing each backup</td>
    </tr>
    <tr>
      <th scope="row"><kbd>Exclude path from file</kbd></th>
      <td>A simple text file where to put the list of files and folders that should not be copied</td>
    </tr>
     <tr>
      <th scope="row"><kbd>Log File</kbd></th>
      <td>A log file</td>
    </tr>
     <tr>
      <th scope="row"><kbd>Execute before</kbd></th>
      <td>A command to execute before the backup</td>
    </tr>
    <tr>
      <th scope="row"><kbd>Execute after</kbd></th>
      <td>A command to execute at the end of the backup</td>
    </tr>
  </tbody>
</table>

<h3 class="mt-5">Schedule fields</h3>
<p class="text-justify">These options take effect only if you enable the scheduler from <kbd>File->scheduler->enable</kbd>.
This will load an instance of the scheduler (pobkupd) at the PC login.</p>
<table class="table">
  <thead>
    <tr>
      <th scope="col">Field</th>
      <th scope="col">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row"><kbd>Every Minute</kbd></th>
      <td>back up every n minutes</td>
    </tr>
    <tr>
      <th scope="row"><kbd>Every Hours</kbd></th>
      <td>back up every n hours</td>
    </tr>
    <tr>
      <th scope="row"><kbd>Every Day at</kbd></th>
      <td>back up every day at this time </td>
    </tr>
   
  </tbody>
</table>
<h2 class="mt-5">Save profile</h2>
<p class="text-justify" class="text-justify">At this point we are ready to save the profile by pressing <kbd>save</kbd>. We can launch our backup from the main window, selecting it from the drop-down menu and pressing <kbd>backup</kbd>
</p>
<img src="imgs/pobkup-linux.png" class="img-fluid"  alt="Linux">
</div><!--end content -->


<?php include('pages/footer.php'); ?>
