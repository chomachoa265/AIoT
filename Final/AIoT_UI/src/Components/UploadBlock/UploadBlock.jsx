import './UploadBlock.scss';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Button } from 'react-bootstrap';
const uploadIcon = () => {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242"></path>
            <path d="M12 12v9"></path>
            <path d="m16 16-4-4-4 4"></path>
        </svg>
    )
}

function UploadBlock(){
    const uploadHandler = (e) => {
        console.log(e.target.files)
        // Create a FormData to POST to backend
        const files = Array.from(e.target.files);
        const formData = new FormData();
        // formData.append("file", null); // key - value
        // Send to Flask
        const response = fetch(`http://localhost:5000/upload`, {
            method: 'POST',
            body: {},
        }).then( res => console.log(res))

    }
    return (
        <div className='upload-block'>
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242"></path>
                <path d="M12 12v9"></path>
                <path d="m16 16-4-4-4 4"></path>
            </svg>
            <p>Click or Drag the files to Upload</p>
            <Button as="a" variant="primary" onClick={() => document.getElementById("upload").click() }>
                Upload Images
            </Button>
            <input id="upload" type="file" onChange={uploadHandler} accept="image/*" hidden multiple />
        </div>
    )
}

export default UploadBlock;