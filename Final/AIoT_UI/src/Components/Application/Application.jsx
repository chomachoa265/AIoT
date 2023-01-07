import * as echarts from 'echarts';
import { Badge, Button, Card, CardGroup, Form, Image, ListGroup, Modal, ProgressBar, Spinner } from 'react-bootstrap';
import { LineBarChart, PieBarChart } from '../Charts/Charts';
import './Application.scss';
import testImage from './../../assets/panorama1.jpg';
import testGradCAMImage from './../../assets/grad_cam_panorama1.jpg';
import CardHeader from 'react-bootstrap/esm/CardHeader';
import { useEffect, useState } from 'react';
import { domain_url } from '../urls';
import UploadBlock from '../UploadBlock/UploadBlock';

function ReposListGroup (props) {
    const items = props.repos.map( (item) =>{
        const baseClass = "list-group-item d-flex justify-content-between align-items-center bg-transparent text-lg-bold"
        const domClass = props.index == item.repo_id ? [baseClass, 'selected'].join(' ') : baseClass;

        return <li key={item.repo_id} className={domClass} onClick={() => props.indexChange(item.repo_id)}>
            {item.name}
            <div>
                <Badge bg={"primary"} pill>
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-images" viewBox="0 0 16 16">
                        <path d="M4.502 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3z"/>
                        <path d="M14.002 13a2 2 0 0 1-2 2h-10a2 2 0 0 1-2-2V5A2 2 0 0 1 2 3a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v8a2 2 0 0 1-1.998 2zM14 2H4a1 1 0 0 0-1 1h9.002a2 2 0 0 1 2 2v7A1 1 0 0 0 15 11V3a1 1 0 0 0-1-1zM2.002 4a1 1 0 0 0-1 1v8l2.646-2.354a.5.5 0 0 1 .63-.062l2.66 1.773 3.71-3.71a.5.5 0 0 1 .577-.094l1.777 1.947V5a1 1 0 0 0-1-1h-10z"/>
                    </svg>
                    {item.number_of_images}
                </Badge>
                <svg className='bi bi-x-lg m-1 delete-btn' xmlns="http://www.w3.org/2000/svg" width="0" height="0" fill="currentColor" viewBox="0 0 16 16" onClick={(e) => props.deleteHandler(e, item.repo_id)}>
                    <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"/>
                </svg>
            </div>
        </li>
    }

    )
    return (
    <ul class="list-group overflow-auto" style={{maxHeight: '600px'}}>
        {items}
    </ul>
    )
}


function ReposCard (props) {

    const [filterStr, setFilterStr] = useState("");

    const [imageData, setImageData] = useState();
    const [repoName, setRepoName]  = useState("");


    const [isProcess, setProcess] = useState(false);
    const [show, setShow] = useState(false);

    
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    const searchHandler = (e) => {
        const filterStr = e.target.value;
        setFilterStr(filterStr)
    }

    const deleteHandler = (e, idx) => {
        e.preventDefault();
        fetch(`${domain_url}/delete/${idx}`, {
            method: 'GET',
        }).then( res => {
            if(res.status == 200) props.fetchRepos();
        })
    }

    const submitHandler = (e) => {
        e.preventDefault();
        if(!isProcess) setProcess(true);
        // Create a FormData to POST to backend
        const data = new FormData();
        data.append("repoName", repoName)
        for (let i = 0; i < imageData.length; i++) {
            data.append("file", imageData[i]);
          }
        // Send to Flask
        fetch(`${domain_url}/api`, {
            method: 'POST',
            body: data,
        }).then( res => res.json())
        .then(() => {
            props.fetchRepos();
            setProcess(false);
            setShow(false);
        })
    } 

    return (
    <Card style={{ width: '20rem', height: '800px'}} bg="dark">
        <Card.Body>
            <Card.Header className='d-flex'>
                <input class="form-control bg-dark text-white" id="myInput" type="text" placeholder="Search.." onChange={searchHandler} />
            </Card.Header>
            <ReposListGroup
                repos={props.repos.filter( repo => repo.name.includes(filterStr))} 
                index={props.index}
                deleteHandler={deleteHandler} 
                indexChange={props.indexChange} />
            <Button 
                variant='primary' 
                className='m-5' 
                style={{
                    position: 'absolute',
                    bottom: '0',
                }}
                onClick={handleShow}>
                Create New Batch
            </Button>
            <Modal show={show} onHide={handleClose} backdrop={'static'}>
                <Modal.Header closeButton className="bg-dark text-white" closeVariant="white">
                    <Modal.Title>Create New Batch</Modal.Title>
                </Modal.Header>
                <Modal.Body className='bg-dark text-white'>
                    <Form>
                        <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
                            <Form.Label>Repository Name</Form.Label>
                            <Form.Control
                                className='bg-dark text-white'
                                type="text"
                                value={repoName}
                                onChange={(e)  => setRepoName(e.currentTarget.value)}
                                placeholder="test-api"
                                autoFocus
                            />
                        </Form.Group>
                        <Form.Group
                        className="mb-3"
                        controlId="exampleForm.ControlTextarea1"
                        >
                            <Form.Label>Image Files</Form.Label><br />
                            <Button variant="primary" onClick={() => document.getElementById('upload').click()}>
                               Choose Images
                            </Button>
                        </Form.Group>
                    </Form>
                </Modal.Body>
                <Modal.Footer className='bg-dark text-white justify-content-center'>
                    <Button variant="primary" onClick={submitHandler} disabled={isProcess}>
                        {isProcess ?                         
                        <Spinner
                            as="span"
                            animation="border"
                            size="sm"
                            role="status"
                            aria-hidden="true"
                        /> : null}
                        {isProcess ? "" : "Process"}
  
                    </Button>
                </Modal.Footer>
            </Modal>
            <input id="upload" type="file" onChange={(e) => setImageData(e.target.files)} accept="image/*" hidden multiple />
        </Card.Body>
    </Card>
    )
}

function Application () {

    const [repos, setRepos] = useState([]);
    const [repoIndex, setRepoIndex] = useState();
    const [chartData, setchartData] = useState({
        image_r: 0,
        image_g: 0,
        image_b: 0,
        lightness: 0,
    });
    const indexChange = (i) => {
        setRepoIndex(i);
    }

    const fetchRepos = () => {
        fetch(`${domain_url}/repos`, {
            method: 'GET',
        }).then((res) => res.json())
        .then((data) => {
            setRepos(data);
            setRepoIndex(data[0].repo_id);
        });
    }
    
    const downloadHandler = () => {
        fetch(`${domain_url}/downloads/${repoIndex}`, {
            method: 'GET',
        }).then((res) => res.blob())
        .then((blob) => {
            const url = window.URL.createObjectURL(new Blob([blob]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute(
            'download',
            `results.zip`,
            );
            document.body.appendChild(link);
            // Start download
            link.click();
            // Clean up and remove the link
            link.parentNode.removeChild(link);
        })
    }
    
    useEffect(() => {
        fetchRepos();
    }, [])

    useEffect(() => {
        fetch(`${domain_url}/chartData/${repoIndex}`, {
            method: 'GET',
        }).then((res) => res.json())
        .then((data) => {
            setchartData(data[0]);
        })
    }, [repoIndex])
    
    return (
        <div className='app-wrapper'>
            <div className='app-results'>
                <div className='results-left'>
                    <ReposCard repos={repos} index={repoIndex} indexChange={indexChange} fetchRepos={fetchRepos}/>
                </div>
                <div className='results-right'>
                    <CardGroup >
                        <Card bg='dark'>
                            <CardHeader>Color Statistic</CardHeader>
                            <CardGroup className='m-3 justify-content-center'>
                                <PieBarChart value={chartData.image_r} label={["Red Value"]} colormap={["#F08080"]}/>
                                <PieBarChart value={chartData.image_g} label={["Green Value"]} colormap={["#90EE90"]}/>
                                <PieBarChart value={chartData.image_b} label={["Blue Value"]} colormap={["#1E90FF"]}/>
                                <PieBarChart value={chartData.lightness} label={["Lightness"]} colormap={["#CCC"]}/>
                            </CardGroup>
                        </Card>
                    </CardGroup>
                    <div className="results-images">
                        <CardGroup className="custom-flex-group">
                            <Card bg='dark' className='mt-2' style={{height: '100%'}}>
                                <CardHeader>Panorama</CardHeader>
                                <Card.Body className='d-flex align-items-center justify-content-center' style={{height: '0'}} >
                                    <Image fluid={true} src={`${domain_url}/media/${repoIndex}/results/panorama.jpg`} alt=""  />
                                </Card.Body>
                            </Card>
                            <Card bg='dark' className='mx-2 mt-2' style={{height: '100%'}}>
                                <CardHeader>Panorama(enhancement)</CardHeader>
                                <Card.Body className='d-flex align-items-center justify-content-center' style={{height: '0'}}>
                                    <Image fluid={true} src={`${domain_url}/media/${repoIndex}/results/enhanced_panorama.jpg`} alt="" />
                                </Card.Body>
                            </Card>
                            <Card bg='dark' className='mt-2' style={{height: '100%'}}>
                                <CardHeader>Grad-CAM</CardHeader>
                                <Card.Body className='d-flex align-items-center justify-content-center' style={{height: '0'}}>
                                    <Image fluid={true} src={`${domain_url}/media/${repoIndex}/results/grad_cam_panorama.jpg`} alt="" />
                                </Card.Body>
                            </Card>
                        </CardGroup>
                    </div>
                    <div className='adjust-images'>
                        {/* <Button variant='primary'>
                            Lightness adjustment
                        </Button> */}
                        <Button 
                            variant='primary' 
                            onClick={downloadHandler}>
                            Download result images
                        </Button>
                    </div>
                </div>
            </div>
        </div>
    )
}


export default Application;