// src/pages/Resources.tsx
import React from 'react';
import { Outlet } from 'react-router-dom';

const Resources: React.FC = () => {
    return (
        <div>
            <h1>Resources</h1>
            <Outlet />
        </div>
    );
};

export default Resources;