export interface Stats {
    strength: string;
    agility: string;
    vitality: string;
    luck: string;
}
export interface Item {

}
export interface Character {
    nickname: string;
    level: number;
    currentExp: number;
    currency: number;
    stats : Stats;
    equippedItems: {
        [key: string]: Item
    };
    itemStats: Stats;
    characterStats: Stats;
}





const fields = ['url', 'nickname', 'level', 'current_exp', 'currency', 'strength',
            'agility', 'vitality', 'luck', 'total_stats', 'equipped_items']