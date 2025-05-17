import React from 'react';
import { Link } from 'react-router-dom';

const Home: React.FC = () => {
    return (
    <div className="container">
       <div>
            <h1>Find your fur-ever friend, today!</h1>
            <Link to="/login">
                {!localStorage.getItem('user_id') && 
                <button style={{ padding: '10px 20px', fontSize: '16px' }}>
                    First you should Login/Signup!
                </button>
                }
            </Link>
            <Link to="/questionnaire">
                {localStorage.getItem('user_id') && 
                <button style={{ padding: '10px 20px', fontSize: '16px' }}>
                    Fill out the Questionnaire!
                </button>
                }
            </Link>
        </div>
    </div>
    );
};

export default Home;