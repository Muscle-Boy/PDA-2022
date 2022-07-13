// import Form from 'react-bootstrap/Form';
// import Tabs from 'react-bootstrap/Tabs';
// import Tab from 'react-bootstrap/Tab';
// import Sonnet from 'react-bootstrap/Tab';
import React, {useState,useEffect} from 'react';
import './Upload.css';

// #all the actions in the front end must be used to connect to the backend // form > function > jsonify > post to api

function Upload() {
    const [title, setTitle] = useState("");
    const [textinput, settextinput] = useState("");
    const [CheckedBox1, setCheckedBox1] = useState(false);
    const [CheckedBox2, setCheckedBox2] = useState(false);
    const [Message, setMessage] = useState("");
    const [output, setOutput] = useState("");

    

  let handleSubmit = async (e) => {
    e.preventDefault();
    const data = {}
    data["form"] = {
        "title": title,
        "textinput": textinput,
        "CheckedBox1": CheckedBox1,
        "CheckedBox2": CheckedBox2,
        "Message":Message,
        "output":output,
     
    }
    console.log(data)
    try{
      setMessage("Loading... ");
  let res = await fetch("http://127.0.0.1:5000/app/upload",{
    method: "POST",
    body: JSON.stringify(data),
  });
  let resJson =  await res.json();

  if(res.status === 200 ){
    setTitle("");
    settextinput("");
    setMessage("Crawled successfully");
    // setOutput()
    
    
    console.log(resJson);
  }
  else{
    setMessage("Some error occured");
    // setOutput("Error occured while obtaining sentence, please try again later");
    console.log("error")
  }
  if(resJson.success){
    setOutput(resJson.result);
  }
  else{
    setOutput("Error occurred while obtaining sentence, please try again later");
  }

  // let out = await fetch;
  // let resout = await out.json;
  // console.log(res.result[0].summary_text);
  // if (resout===200){
  //   console.log("Into IF statement");
  //   setOutput(res.result[0].summary_text);
  // }
  // else{
  //   setOutput("Error occurred while obtaining sentence, please try again later");
  // }
  
    }
catch(err){
    console.log(err);
  }
}

// const Upload = () => {
    // const [key, setKey] = useState('home');
  return(

         <form onSubmit={handleSubmit}>
        <div>
        <input type = "text" value={title} onChange={(e)=>setTitle(e.target.value)} required autoFocus/>
        <label>Title </label>
        </div>
        <div>
        <textarea name="message" value ={textinput} onChange={(e)=>settextinput(e.target.value)}></textarea>
            <label>Text </label>
        </div>
        <div>
        <input type="checkbox" id="vehicle1" value="vehicle1" onClick={()=>{
            setCheckedBox1(!CheckedBox1)
        }} />
        <label for="vehicle1"> Option1</label>
    </div>
    <div>
<input type="checkbox" id="vehicle2" value="vehicle2" onClick={()=>{
    setCheckedBox2(!CheckedBox2)
}} />
<label for="vehicle2"> Option2</label>
</div>
      
      
        <input type="submit" value="Submit"/>
     <div value={Message}>{Message}</div>
     <div>{output}</div>
        </form>
        
    )
  }




  export default Upload;
