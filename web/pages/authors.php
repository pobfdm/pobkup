<script>
	$( document ).ready(function(){
		$('#showContact').click(function(){
				$('#contact').fadeToggle();
			});
		
		});
</script>

<div class="container-fluid" style="margin-top:90px">
<div class="jumbotron jumbotron-home" >
<h3>Authors:</h3>
<p class="lead"><a id="showContact" href="#">Fabio Di Matteo</a></p>
<div id="contact" class="alert alert-secondary" role="alert" style="display:None">
  <img src="imgs/email.png" />
</div>
<hr class="my-4">

<h3>Contributors:</h3>
<p class="lead">You?</p>
<hr class="my-4">

<h3>Translators:</h3>
<p class="lead">You?</p>
<hr class="my-4"> 

<h3>Artist:</h3>
<p class="lead"><a href="https://www.iconfinder.com/Ampeross" target="_blank">Arthur Zaynullin</a></p>
<hr class="my-4"> 
  
</div>

</div><!-- /home content-->
<?php include('pages/footer.php'); ?>
