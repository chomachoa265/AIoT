import logo from './logo.svg';
import './App.scss';
import { AppHeader } from './Components/AppHeader/AppHeader';
import UploadBlock from './Components/UploadBlock/UploadBlock';
import Dashboard from './Components/Dashboard/Dashboard';
import Application from './Components/Application/Application';
import { Route, Routes } from 'react-router';

function App() {
  return (
    <div className="App">
      <AppHeader />
      <div className='app-main'>     
        <Routes>
          <Route path="/dashboard" element={<Dashboard />}></Route>
          <Route path="/application" element={<Application />}></Route>
        </Routes>
      </div>
      <div className='app-footer'>

      </div>
      {/* Footer */}
    </div>
  );
}

export default App;
