import React from 'react';
import { useForm } from "react-hook-form";
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle
} from "@/components/ui/card";
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue
} from "@/components/ui/select";
import {DatePicker} from "@/components/ui/date-picker.tsx";

function setStartDate(date) {
    
}

const Pricer: React.FC = () => {
    const form = useForm({
        defaultValues: {
            productName: '',
            price: '',
            derivativeType: '',
            asset: '',
            strike: '',
        },
    });

    const onSubmit = (data: any) => {
        console.log('Form data:', data);
    };

    let startDate;
    return (
        <div>
            <div className="h-screen w-screen flex justify-center items-center">
                <Card className="w-[700px] h-auto">
                    <CardHeader>
                        <CardTitle className="text-5xl">Pricer</CardTitle>
                        <CardDescription>Enter details to price a product.</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <Form {...form}>
                            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">

                                {/* Derivative Type Select Field */}
                                <FormField
                                    control={form.control}
                                    name="derivativeType"
                                    render={({field}) => (
                                        <FormItem>
                                            <FormLabel>Derivative Type</FormLabel>
                                            <Select onValueChange={field.onChange} defaultValue={field.value}>
                                                <FormControl>
                                                    <SelectTrigger>
                                                        <SelectValue placeholder="Select type"/>
                                                    </SelectTrigger>
                                                </FormControl>
                                                <SelectContent>
                                                    <SelectItem value="option">Option</SelectItem>
                                                </SelectContent>
                                            </Select>
                                            <FormMessage/>
                                        </FormItem>
                                    )}
                                />


                                {/* Asset Select Field */}
                                <div className="flex space-x-4">
                                    {/* Expiry Field */}
                                    <FormField
                                        control={form.control}
                                        name="assetType"
                                        render={({field}) => (
                                            <FormItem className="flex-1">
                                                <FormLabel>Asset Type</FormLabel>
                                                <Select onValueChange={field.onChange} defaultValue={field.value}>
                                                    <FormControl>
                                                        <SelectTrigger>
                                                            <SelectValue placeholder="Select asset Type"/>
                                                        </SelectTrigger>
                                                    </FormControl>
                                                    <SelectContent>
                                                        <SelectItem value="stock">Stock</SelectItem>
                                                    </SelectContent>
                                                </Select>
                                                <FormMessage/>
                                            </FormItem>
                                        )}
                                    />
                                    {/* Price Field */}
                                    <FormField
                                        name="asset"
                                        control={form.control}
                                        render={({field}) => (
                                            <FormItem className="flex-1">
                                                <FormLabel>Asset</FormLabel>
                                                <FormControl>
                                                    <Input placeholder="AAPL" {...field} />
                                                </FormControl>
                                                <FormMessage/>
                                            </FormItem>
                                        )}
                                    />
                                </div>

                                {/* Row of Two Fields */}
                                <div className="flex space-x-4 w-full">
                                    {/* Expiry Field */}
                                    <FormField
                                        name="expiry"
                                        control={form.control}
                                        render={({field}) => (
                                            <FormItem className="flex-1">
                                                <FormLabel>Maturity</FormLabel>
                                                <FormControl>
                                                    <Input
                                                        placeholder="Select Maturity (in years) ex: 2.0"
                                                        {...field}
                                                        className="w-full"  // Ensure the input takes full width of the container
                                                    />
                                                </FormControl>
                                                <FormMessage/>
                                            </FormItem>
                                        )}
                                    />

                                    {/* Date Field */}
                                    <FormItem className="flex-1">
                                        <FormLabel>Expiry Date</FormLabel>
                                        <FormControl>
                                            <DatePicker
                                                selected={startDate}
                                                onChange={(date) => {
                                                    setStartDate(date);
                                                }}
                                                className="w-full"  // Ensure the date picker takes full width of the container
                                            />
                                        </FormControl>
                                        <FormMessage/>
                                    </FormItem>
                                </div>
                                {/* Row of Two Fields */}
                                <div className="flex space-x-4">
                                    {/* Spot Field */}
                                    <FormField
                                        name="spot"
                                        control={form.control}
                                        render={({field}) => (
                                            <FormItem className="flex-1">
                                                <FormLabel>Spot</FormLabel>
                                                <FormControl>
                                                    <Input placeholder="Set Spot" {...field} />
                                                </FormControl>
                                                <FormMessage/>
                                            </FormItem>
                                        )}
                                    />
                                    {/* Price Field */}
                                    <FormField
                                        name="volatility"
                                        control={form.control}
                                        render={({field}) => (
                                            <FormItem className="flex-1">
                                                <FormLabel>Volatility</FormLabel>
                                                <FormControl>
                                                    <Input placeholder="0.20" {...field} />
                                                </FormControl>
                                                <FormMessage/>
                                            </FormItem>
                                        )}
                                    />
                                </div>

                                <div className="flex space-x-4">
                                    {/* Spot Field */}
                                    <FormField
                                        name="riskFreeRate"
                                        control={form.control}
                                        render={({field}) => (
                                            <FormItem className="flex-1">
                                                <FormLabel>Risk-Free rate</FormLabel>
                                                <FormControl>
                                                    <Input placeholder="Set Risk-Free rate" {...field} />
                                                </FormControl>
                                                <FormMessage/>
                                            </FormItem>
                                        )}
                                    />
                                    {/* Price Field */}
                                    <FormField
                                        name="dividendYield"
                                        control={form.control}
                                        render={({field}) => (
                                            <FormItem className="flex-1">
                                                <FormLabel>Dividend Yield</FormLabel>
                                                <FormControl>
                                                    <Input placeholder="set Dividend Yield" {...field} />
                                                </FormControl>
                                                <FormMessage/>
                                            </FormItem>
                                        )}
                                    />
                                </div>

                                {/* Row of Two Fields */}
                                <div className="flex space-x-4">
                                    {/* Strike Field */}
                                    <FormField
                                        name="strike"
                                        control={form.control}
                                        render={({field}) => (
                                            <FormItem className="flex-1">
                                                <FormLabel>Strike</FormLabel>
                                                <FormControl>
                                                    <Input placeholder="Set Strike" {...field} />
                                                </FormControl>
                                                <FormMessage/>
                                            </FormItem>
                                        )}
                                    />
                                    {/* Price Field */}
                                    <FormField
                                        name="price"
                                        control={form.control}
                                        render={({field}) => (
                                            <FormItem className="flex-1">
                                                <FormLabel>.</FormLabel>
                                                <FormControl>
                                                    <Input placeholder="0.02 ITMF" {...field} />
                                                </FormControl>
                                                <FormMessage/>
                                            </FormItem>
                                        )}
                                    />
                                </div>

                                {/* Row of Two Fields */}
                                {/*<div className="flex space-x-4">*/}
                                {/*    /!* Strike Field *!/*/}
                                {/*    <FormField*/}
                                {/*        control={form.control}*/}
                                {/*        name="notional"*/}
                                {/*        render={({field}) => (*/}
                                {/*            <FormItem className="flex-1">*/}
                                {/*                <FormLabel>Notional</FormLabel>*/}
                                {/*                <Select onValueChange={field.onChange} defaultValue={field.value}>*/}
                                {/*                    <FormControl>*/}
                                {/*                        <SelectTrigger>*/}
                                {/*                            <SelectValue placeholder="Select currency"/>*/}
                                {/*                        </SelectTrigger>*/}
                                {/*                    </FormControl>*/}
                                {/*                    <SelectContent>*/}
                                {/*                        <SelectItem value="usd">USD</SelectItem>*/}
                                {/*                        <SelectItem value="eur">EUR</SelectItem>*/}
                                {/*                        <SelectItem value="chf">CHF</SelectItem>*/}
                                {/*                    </SelectContent>*/}
                                {/*                </Select>*/}
                                {/*                <FormMessage/>*/}
                                {/*            </FormItem>*/}
                                {/*        )}*/}
                                {/*    />*/}
                                {/*    /!* Price Field *!/*/}
                                {/*    <FormField*/}
                                {/*        name="price"*/}
                                {/*        control={form.control}*/}
                                {/*        render={({field}) => (*/}
                                {/*            <FormItem className="flex-1">*/}
                                {/*                <FormLabel>Amount</FormLabel>*/}
                                {/*                <FormControl>*/}
                                {/*                    <Input placeholder="200,000" {...field} />*/}
                                {/*                </FormControl>*/}
                                {/*                <FormMessage/>*/}
                                {/*            </FormItem>*/}
                                {/*        )}*/}
                                {/*    />*/}
                                {/*</div>*/}
                                <FormField
                                    control={form.control}
                                    name="model"
                                    render={({field}) => (
                                        <FormItem>
                                            <FormLabel>Model/Methodology</FormLabel>
                                            <Select onValueChange={field.onChange} defaultValue={field.value}>
                                                <FormControl>
                                                    <SelectTrigger>
                                                        <SelectValue placeholder="Select model"/>
                                                    </SelectTrigger>
                                                </FormControl>
                                                <SelectContent>
                                                    <SelectItem value="blackScholes">Black Scholes</SelectItem>
                                                    <SelectItem value="monteCarlo">Monte Carlo</SelectItem>

                                                </SelectContent>
                                            </Select>
                                            <FormMessage/>
                                        </FormItem>
                                    )}
                                />


                                <div className="flex space-x-40">
                                    <Button variant="secondary" type="button" className="w-full">
                                        Clear
                                    </Button>

                                    <Button type="submit" className="w-full">
                                        Submit
                                    </Button>
                                </div>

                            </form>
                        </Form>
                    </CardContent>
                    <CardFooter>
                        <p className="text-sm text-gray-500">Ensure all fields are filled before submitting.</p>
                    </CardFooter>
                </Card>
            </div>
        </div>
    );
};

export default Pricer;