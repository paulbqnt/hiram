// src/pages/Home.tsx
import React from 'react';
import { Outlet } from 'react-router-dom';
import {Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle} from "@/components/ui/card.tsx";
import Navbar from "@/components/Navbar.tsx";

const Home: React.FC = () => {
    return (
        <div>
            <Navbar/>
            <h1>Home</h1>
            <Outlet />

            <Card className="flex flex-col justify-between text-green-500">
                <CardHeader>
                    <div>
                        <CardTitle>
                            Home
                        </CardTitle>
                        <CardDescription>
                            This is a description
                        </CardDescription>
                    </div>
                </CardHeader>
                <CardContent>
                    <p>test, ceci est la description</p>
                </CardContent>
                <CardFooter>
                    <button>View Recipe</button>
                    {<p>vegan</p>}
                </CardFooter>
            </Card>
        </div>
    );
};

export default Home;