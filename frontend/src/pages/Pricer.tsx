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
                                                    <SelectItem value="future">Future</SelectItem>
                                                    <SelectItem value="forward">Forward</SelectItem>
                                                    <SelectItem value="swap">Swap</SelectItem>
                                                </SelectContent>
                                            </Select>
                                            <FormMessage/>
                                        </FormItem>
                                    )}
                                />

                                {/* Asset Select Field */}
                                <FormField
                                    control={form.control}
                                    name="asset"
                                    render={({field}) => (
                                        <FormItem>
                                            <FormLabel>Asset</FormLabel>
                                            <Select onValueChange={field.onChange} defaultValue={field.value}>
                                                <FormControl>
                                                    <SelectTrigger>
                                                        <SelectValue placeholder="Select asset"/>
                                                    </SelectTrigger>
                                                </FormControl>
                                                <SelectContent>
                                                    <SelectItem value="equity">Equity</SelectItem>
                                                    <SelectItem value="fx">FX</SelectItem>
                                                    <SelectItem value="commodity">Commodity</SelectItem>
                                                    <SelectItem value="rates">Rates</SelectItem>
                                                </SelectContent>
                                            </Select>
                                            <FormMessage/>
                                        </FormItem>
                                    )}
                                />

                                {/* Row of Two Fields */}
                                <div className="flex space-x-4">
                                    {/* Expiry Field */}
                                    <FormField
                                        name="expiry"
                                        control={form.control}
                                        render={({field}) => (
                                            <FormItem className="flex-1">
                                                <FormLabel>Expiry</FormLabel>
                                                <FormControl>
                                                    <Input placeholder="Select Expiry" {...field} />
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
                                                <FormLabel>Date</FormLabel>
                                                <FormControl>
                                                    <Input placeholder="01/01/2025" {...field} />
                                                </FormControl>
                                                <FormMessage/>
                                            </FormItem>
                                        )}
                                    />
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
                                                    <Input placeholder="01/01/2025" {...field} />
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
                                <div className="flex space-x-4">
                                    {/* Strike Field */}
                                    <FormField
                                        control={form.control}
                                        name="notional"
                                        render={({field}) => (
                                            <FormItem className="flex-1">
                                                <FormLabel>Notional</FormLabel>
                                                <Select onValueChange={field.onChange} defaultValue={field.value}>
                                                    <FormControl>
                                                        <SelectTrigger>
                                                            <SelectValue placeholder="Select asset"/>
                                                        </SelectTrigger>
                                                    </FormControl>
                                                    <SelectContent>
                                                        <SelectItem value="usd">USD</SelectItem>
                                                        <SelectItem value="eur">EUR</SelectItem>
                                                        <SelectItem value="chf">CHF</SelectItem>
                                                    </SelectContent>
                                                </Select>
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
                                                <FormLabel>Amount</FormLabel>
                                                <FormControl>
                                                    <Input placeholder="0.02 ITMF" {...field} />
                                                </FormControl>
                                                <FormMessage/>
                                            </FormItem>
                                        )}
                                    />
                                </div>
                                <FormField
                                    control={form.control}
                                    name="model"
                                    render={({field}) => (
                                        <FormItem>
                                            <FormLabel>Model</FormLabel>
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