// import Form from 'react-bootstrap/Form';
// import Tabs from 'react-bootstrap/Tabs';
// import Tab from 'react-bootstrap/Tab';
// import Sonnet from 'react-bootstrap/Tab';
import React from 'react';
import './Upload.css';


const Upload = () => {
    // const [key, setKey] = useState('home');
  
    return(

         <form action="login" method="post">
                        
                    
        <div>
        <input type = "text" name="" required autofocus/>
        <label>Title </label>
        </div>
        <div>
        <textarea name="message"></textarea>
            <label>Text </label>
        </div>
        <div>
        <input type="checkbox" id="vehicle1" name="vehicle1" value="Bike"/>
<label for="vehicle1"> I have a bike</label>
    </div>
    <div>
<input type="checkbox" id="vehicle2" name="vehicle2" value="Car"/>
<label for="vehicle2"> I have a car</label>
</div><div>
<input type="checkbox" id="vehicle3" name="vehicle3" value="Boat"/>
<label for="vehicle3"> I have a boat</label><br></br>
        </div>
      
      
        <input type="submit" value="Submit"/>
        </form>
       

    )
  }
  export default Upload;
