import React, {useState, useEffect} from "react";

/* Import Components */
import CheckBox from "./FormElements/Checkbox";
import Select from "./FormElements/Select";
import Button from "./FormElements/Button";

const Options = (props) => {
  const {setConfig, uploadFiles, config, files} = props
  const [data, setData] = useState({platform: "Dark Web", visualisations: ["Fake News", 
  "Stance Detection", "Summary", "Word Cloud","Topic Modelling", "NER and Relation"]})

  const platformOptions = ["Dark Web", "Twitter", "Facebook", "HardWareZone", "Reddit"]

  const visualisationOptions = ["Fake News", "Stance Detection", "Summary", "Word Cloud", "Topic Modelling", "NER and Relation"]

  const handleInput = (e) => {
    let value = e.target.value;
    const visualisationData = data.visualisations
    setData({
      platform: value, visualisations: visualisationData 
    });
  }

  const handleCheckBox = (e) => {
    //new selection is the option that is being checked or unchecked
    const newSelection = e.target.value;
    let newSelectionArray;
    const platformData = data.platform;

    if (data.visualisations.indexOf(newSelection) > -1) {
      newSelectionArray = data.visualisations.filter(
        s => s !== newSelection
      );
    } else {
      newSelectionArray = [...data.visualisations, newSelection];
    }

    setData({
      platform: platformData, visualisations: newSelectionArray
    });
  }

  const handleNewData = (e) => {
    return (setConfig(data))
  }

  const handleFormSubmit = (e) => {
    e.preventDefault();
    return (setConfig(data))
    // setConfig(JSON.stringify(data))
    return (uploadFiles())
  }

 const handleClearForm = (e) => {
    e.preventDefault();
    setData({
        platform: "",
        visualisations: []
    });
  }

    return (
      <form className="container-fluid" onSubmit={handleFormSubmit}>
        {/* Platform Selection */}
        <Select
          title={"Platform"}
          name={"platform"}
          options={platformOptions}
          value={data.platform}
          placeholder={"Select Platform"}
          handleChange={handleInput}
        />{" "}
        
        {/* Visualisation Section */}
        <CheckBox
          title={"Visualisations"}
          name={"visualisations"}
          options={visualisationOptions}
          selectedOptions={data.visualisations}
          handleChange={handleCheckBox}
        />{" "}
        
        {/*Submit */}
        <Button
          action={handleFormSubmit}
          type={"primary"}
          title={"Apply"}
          style={buttonStyle}
        />{" "}
        
        {/* Clear the form */}
        <Button
          action={handleClearForm}
          type={"secondary"}
          title={"Clear"}
          style={buttonStyle}
        />{" "}
        
      </form>
    );
}

const buttonStyle = {
  margin: "10px 10px 10px 10px"
};

export default Options;