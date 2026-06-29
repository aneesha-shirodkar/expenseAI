export default function FilterBar({  month,setMonth,category,setCategory}) 
{

    return (

        <div className="flex gap-4 mb-6 overflow-y-auto">

            <select
                value={month}
                onChange={e =>
                    setMonth(e.target.value)
                }
                className="border rounded p-2"
            >

                <option value="">
                    All Months
                </option>

                <option value="1">Jan</option>
                <option value="2">Feb</option>
                <option value="3">Mar</option>
                <option value="4">Apr</option>
                <option value="5">May</option>
                <option value="6">Jun</option>
                <option value="7">Jul</option>
                <option value="8">Aug</option>
                <option value="9">Sep</option>
                <option value="10">Oct</option>
                <option value="11">Nov</option>
                <option value="12">Dec</option>

            </select>

            <select
                value={category}
                onChange={e =>
                    setCategory(e.target.value)
                }
                className="border rounded p-2"
            >

                <option value="">
                    All Categories
                </option>

                <option value="Food">
                    Food
                </option>

                <option value="Fuel">
                    Fuel
                </option>

                <option value="Shopping">
                    Shopping
                </option>

                <option value="Groceries">
                    Groceries
                </option>

            </select>

        </div>
    );
}