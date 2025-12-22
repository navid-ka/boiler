import { useEffect, useState } from "react"
import axios from "axios"

import { CreateItemCard } from "./components/CreateItemCard"
import { ItemCard } from "./components/ItemCard"

function App() {
	const [items, setItems] = useState([])

	const getItems = async () => {
		const res = await axios.get("/api/v1/items/")
		setItems(res.data)
	}

	useEffect(() => {
		getItems()
	}, [])

	return (
		<div className="flex mt-10 ml-10 flex-col gap-4 mx-auto ">
			<CreateItemCard refreshItems={getItems} />

			{items.map((item) => (
				<ItemCard
					key={item.id}
					id={item.id}
					title={item.title}
					description={item.description}
					refreshItems={getItems}
				/>
			))}
		</div>
	)
}

export default App
