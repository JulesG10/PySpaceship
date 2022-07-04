
document.addEventListener('DOMContentLoaded', () => {
    let $ = (el) => document.getElementById(el)
    let currentActive = 'home';

    function changePage(next) {
        $(currentActive).classList.remove('active')
        $(currentActive).classList.add('text-white')
        $('page-'+currentActive).hidden = true;

        $(next).classList.remove('text-white')
        $(next).classList.add('active')
        $('page-'+next).hidden = false;
        
        currentActive = next;
    }

    function handleClickPage(e)
    {
        e.preventDefault();
        changePage(e.target.id);
    }

    // $('apiref').addEventListener('click', handleClickPage);
    $('home').addEventListener('click', handleClickPage);
    $('lic').addEventListener('click', handleClickPage);
    $('game').addEventListener('click', handleClickPage);
    $('download').addEventListener('click',(e)=>{
        window.open('./SpaceShip-snapshot_v1.6.7.zip', '_blank');
    })
})