imp = document.getElementById("pageSelect")

imp.onkeyup = event => {
    if(event.keyCode == 13){
        event.preventDefault();
        if (imp.value > 0) { 
            window.location.href = imp.value
        }
    }
}