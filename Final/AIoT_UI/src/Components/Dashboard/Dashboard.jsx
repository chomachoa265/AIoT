import * as echarts from 'echarts';
import { useEffect, useState } from 'react';
import { Badge, Button, Card, CardGroup, ListGroup } from 'react-bootstrap';
import { LineBarChart, PieBarChart } from '../Charts/Charts';
import { domain_url } from '../urls';
import './Dashboard.scss';

function CountCard (props) {
    return (
    <Card style={{ width: '15rem', height: '10rem' }} bg="dark">
        <Card.Body>
            <Card.Text className='text-lb-bold'>{props.name}</Card.Text>
            <Card.Title className='text-lb-bold size-xl'>
                {props.count}
            </Card.Title>
        </Card.Body>
    </Card>
    )
}

function StatCard (props) {
    const chartData = props.chartData;
    return (
    <Card style={{ width: '68rem'}} bg="dark">
        <Card.Body>
            <Card.Header>Overall Statistics</Card.Header>
            <Card.Body>
                <Card.Text className='text-lb-bold'>Average Color Values</Card.Text>
                <CardGroup className='m-3'>
                    <PieBarChart value={chartData == null ? 0 : chartData.avg_r} label={["Red Value"]} colormap={["#F08080"]}/>
                    <PieBarChart value={chartData == null ? 0 : chartData.avg_g} label={["Green Value"]} colormap={["#90EE90"]}/>
                    <PieBarChart value={chartData == null ? 0 : chartData.avg_b} label={["Blue Value"]} colormap={["#1E90FF"]}/>
                    <PieBarChart value={chartData == null ? 0 : chartData.avg_lightness} label={["Lightness"]} colormap={["#CCC"]}/>
                </CardGroup>
                <Card.Text className='text-lb-bold m-0'>RGBL Analysis</Card.Text>
                <CardGroup>
                    <LineBarChart colormap={["#F08080", "#90EE90", "#1E90FF"]} />
                </CardGroup>
            </Card.Body>
        </Card.Body>
    </Card>
    )
}

function Dashboard () {
    const [countData, setCountData] = useState(null);
    const [chartData, setChartData] = useState(null);
    useEffect( () =>{
        fetch(`${domain_url}/dashboardData`, {
            method: 'GET',
        }).then((res) => res.json())
        .then((data) => {
            setCountData(data)
        })

        fetch(`${domain_url}/dashboardChartData`, {
            method: 'GET',
        }).then((res) => res.json())
        .then((data) => {
           setChartData(data)
        })

    }, [])
    console.log(countData);
    return (
        <div className='app-wrapper'>
            <div className='app-dashboard'>
                <div className='dashboard-up'>
                    <CountCard name="Total Repositorys" count={countData == null ? 0 : countData.total_repos} />
                    <CountCard name="Avg. Images" count={countData == null ? 0 : countData.avg_images} />
                    <CountCard name="Avg. Lightness" count={countData == null ? 0 : countData.avg_lightness} />
                    <CountCard name="Downloads" count={countData == null ? 0 : countData.total_downloads} />
                </div>
                <div className='dashboard-statistic'>
                    <StatCard chartData={chartData}/>
                </div>
            </div>
        </div>
    )
}


export default Dashboard;