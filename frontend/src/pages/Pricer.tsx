// src/pages/Pricer.tsx
import React from 'react';
import { Outlet } from 'react-router-dom';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select.tsx";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card.tsx";

const Pricer: React.FC = () => {
    return (
        <div>
            <div className="h-screen w-screen flex justify-center items-center">

                <Card className="w-[700px] h-[900px]">
                    <CardHeader className="text-5xl">
                        <CardTitle>Pricer</CardTitle>
                    </CardHeader>
                </Card>
            </div>





        </div>


    );
};

export default Pricer;