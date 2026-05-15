function toggleFaq(i){
  const body=document.getElementById('fa-body-'+i);
  const arrow=document.getElementById('fa-'+i);
  const isOpen=body.classList.contains('open');
  document.querySelectorAll('.faq-a').forEach(el=>el.classList.remove('open'));
  document.querySelectorAll('.faq-arrow').forEach(el=>el.classList.remove('open'));
  if(!isOpen){body.classList.add('open');arrow.classList.add('open');}
}
// Open first FAQ by default
toggleFaq(0);
