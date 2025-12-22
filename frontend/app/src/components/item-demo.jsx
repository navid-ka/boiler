import { Plus, Minus } from "lucide-react"

import { Button } from "@/components/ui/button"
import {
  Item,
  ItemActions,
  ItemContent,
  ItemDescription,
  ItemMedia,
  ItemTitle,
} from "@/components/ui/item"

export function ItemCard() {
  return (
    <div className="flex w-full max-w-lg flex-col gap-6">
      <Item variant="outline">
        <ItemContent>
          <ItemTitle>Evil Rabbit</ItemTitle>
          <ItemDescription>Last seen 5 months ago</ItemDescription>
        </ItemContent>
        <ItemActions>
          <Button
            size="icon-sm"
            variant="outline"
            className="rounded-full"
            aria-label="Invite"
          >
            <Plus />
          </Button>
          <Button
            size="icon-sm"
            variant="outline"
            className="rounded-full"
            aria-label="Invite"
          >
            <Minus />
          </Button>
        </ItemActions>
      </Item>
    </div>
  )
}
