export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export type Database = {
  public: {
    Tables: {
      active_buy_sell: {
        Row: {
          buy_or_sell: boolean
          expirey: string | null
          has_been_processed: boolean | null
          Id: number
          orderId: string | null
          price: number
          quantity: number
          stockId: number
          time_posted: string
          userId: string
        }
        Insert: {
          buy_or_sell?: boolean
          expirey?: string | null
          has_been_processed?: boolean | null
          Id?: number
          orderId?: string | null
          price?: number
          quantity?: number
          stockId: number
          time_posted: string
          userId: string
        }
        Update: {
          buy_or_sell?: boolean
          expirey?: string | null
          has_been_processed?: boolean | null
          Id?: number
          orderId?: string | null
          price?: number
          quantity?: number
          stockId?: number
          time_posted?: string
          userId?: string
        }
        Relationships: [
          {
            foreignKeyName: "active_buy_sell_stockId_fkey"
            columns: ["stockId"]
            isOneToOne: false
            referencedRelation: "stock_info"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "active_buy_sell_userId_fkey"
            columns: ["userId"]
            isOneToOne: false
            referencedRelation: "profiles"
            referencedColumns: ["userId"]
          }
        ]
      }
      contributors: {
        Row: {
          description: string
          discordUserID: string | null
          githubUsername: string | null
          id: number
          image: string | null
          name: string
          role: string | null
          twitterUsername: string | null
        }
        Insert: {
          description?: string
          discordUserID?: string | null
          githubUsername?: string | null
          id?: number
          image?: string | null
          name: string
          role?: string | null
          twitterUsername?: string | null
        }
        Update: {
          description?: string
          discordUserID?: string | null
          githubUsername?: string | null
          id?: number
          image?: string | null
          name?: string
          role?: string | null
          twitterUsername?: string | null
        }
        Relationships: []
      }
      flags: {
        Row: {
          description: string | null
          id: number
          image: string | null
          name: string
          type: string
        }
        Insert: {
          description?: string | null
          id?: number
          image?: string | null
          name?: string
          type: string
        }
        Update: {
          description?: string | null
          id?: number
          image?: string | null
          name?: string
          type?: string
        }
        Relationships: []
      }
      inactive_buy_sell: {
        Row: {
          buy_or_sell: boolean
          completed: boolean
          delisted_time: string
          expirey: string | null
          Id: number
          orderId: string | null
          price: number
          quantity: number
          stockId: number
          time_posted: string
          userId: string
        }
        Insert: {
          buy_or_sell?: boolean
          completed?: boolean
          delisted_time?: string
          expirey?: string | null
          Id?: number
          orderId?: string | null
          price?: number
          quantity?: number
          stockId: number
          time_posted?: string
          userId: string
        }
        Update: {
          buy_or_sell?: boolean
          completed?: boolean
          delisted_time?: string
          expirey?: string | null
          Id?: number
          orderId?: string | null
          price?: number
          quantity?: number
          stockId?: number
          time_posted?: string
          userId?: string
        }
        Relationships: [
          {
            foreignKeyName: "inactive_buy_sell_stockId_fkey"
            columns: ["stockId"]
            isOneToOne: false
            referencedRelation: "stock_info"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "inactive_buy_sell_userId_fkey"
            columns: ["userId"]
            isOneToOne: false
            referencedRelation: "profiles"
            referencedColumns: ["userId"]
          }
        ]
      }
      market_State: {
        Row: {
          changed_last: string
          id: number
          state: boolean
        }
        Insert: {
          changed_last: string
          id?: number
          state?: boolean
        }
        Update: {
          changed_last?: string
          id?: number
          state?: boolean
        }
        Relationships: []
      }
      portfolio: {
        Row: {
          price_avg: number
          quantity: number
          stockId: number
          userId: string
        }
        Insert: {
          price_avg?: number
          quantity?: number
          stockId?: number
          userId: string
        }
        Update: {
          price_avg?: number
          quantity?: number
          stockId?: number
          userId?: string
        }
        Relationships: [
          {
            foreignKeyName: "portfolio_stockId_fkey"
            columns: ["stockId"]
            isOneToOne: false
            referencedRelation: "stock_info"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "portfolio_userId_fkey"
            columns: ["userId"]
            isOneToOne: false
            referencedRelation: "profiles"
            referencedColumns: ["userId"]
          }
        ]
      }
      profiles: {
        Row: {
          balance: number
          comments: string[] | null
          image: string | null
          joined_at: string
          networth: number
          userId: string
          username: string
        }
        Insert: {
          balance?: number
          comments?: string[] | null
          image?: string | null
          joined_at: string
          networth?: number
          userId: string
          username: string
        }
        Update: {
          balance?: number
          comments?: string[] | null
          image?: string | null
          joined_at?: string
          networth?: number
          userId?: string
          username?: string
        }
        Relationships: [
          {
            foreignKeyName: "profiles_userId_fkey"
            columns: ["userId"]
            isOneToOne: true
            referencedRelation: "users"
            referencedColumns: ["id"]
          }
        ]
      }
      rel_user_flag: {
        Row: {
          flagId: number
          userId: string
        }
        Insert: {
          flagId?: number
          userId: string
        }
        Update: {
          flagId?: number
          userId?: string
        }
        Relationships: [
          {
            foreignKeyName: "rel_user_flag_flagId_fkey"
            columns: ["flagId"]
            isOneToOne: false
            referencedRelation: "flags"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "rel_user_flag_userId_fkey"
            columns: ["userId"]
            isOneToOne: false
            referencedRelation: "profiles"
            referencedColumns: ["userId"]
          }
        ]
      }
      stock_info: {
        Row: {
          description: string | null
          id: number
          image: string | null
          name: string
          total_shares: number
        }
        Insert: {
          description?: string | null
          id?: number
          image?: string | null
          name: string
          total_shares?: number
        }
        Update: {
          description?: string | null
          id?: number
          image?: string | null
          name?: string
          total_shares?: number
        }
        Relationships: []
      }
      stock_price: {
        Row: {
          stock_price: number
          stockId: number
        }
        Insert: {
          stock_price?: number
          stockId?: number
        }
        Update: {
          stock_price?: number
          stockId?: number
        }
        Relationships: [
          {
            foreignKeyName: "stock_price_stockId_fkey"
            columns: ["stockId"]
            isOneToOne: true
            referencedRelation: "stock_info"
            referencedColumns: ["id"]
          }
        ]
      }
      stock_price_history_daily: {
        Row: {
          changed_at: string
          id: number
          price: number
          stockId: number
        }
        Insert: {
          changed_at: string
          id?: number
          price: number
          stockId: number
        }
        Update: {
          changed_at?: string
          id?: number
          price?: number
          stockId?: number
        }
        Relationships: [
          {
            foreignKeyName: "public_stock_price_history_daily_stockId_fkey"
            columns: ["stockId"]
            isOneToOne: false
            referencedRelation: "stock_info"
            referencedColumns: ["id"]
          }
        ]
      }
      stock_price_history_monthly: {
        Row: {
          average_price: number
          closing_price: number
          highest_price: number
          id: number
          lowest_price: number
          opening_price: number
          starting_hour: string
          stockId: number
          volume_of_sales: number
        }
        Insert: {
          average_price: number
          closing_price: number
          highest_price: number
          id?: number
          lowest_price: number
          opening_price: number
          starting_hour: string
          stockId: number
          volume_of_sales: number
        }
        Update: {
          average_price?: number
          closing_price?: number
          highest_price?: number
          id?: number
          lowest_price?: number
          opening_price?: number
          starting_hour?: string
          stockId?: number
          volume_of_sales?: number
        }
        Relationships: [
          {
            foreignKeyName: "public_stock_price_history_monthly_stockId_fkey"
            columns: ["stockId"]
            isOneToOne: false
            referencedRelation: "stock_info"
            referencedColumns: ["id"]
          }
        ]
      }
      stock_price_history_weekly: {
        Row: {
          average_price: number
          closing_price: number
          highest_price: number
          id: number
          lowest_price: number
          opening_price: number
          starting_hour: string
          stockId: number
          volume_of_sales: number
        }
        Insert: {
          average_price: number
          closing_price: number
          highest_price: number
          id?: number
          lowest_price: number
          opening_price: number
          starting_hour: string
          stockId: number
          volume_of_sales: number
        }
        Update: {
          average_price?: number
          closing_price?: number
          highest_price?: number
          id?: number
          lowest_price?: number
          opening_price?: number
          starting_hour?: string
          stockId?: number
          volume_of_sales?: number
        }
        Relationships: [
          {
            foreignKeyName: "public_stock_price_history_weekly_stockId_fkey"
            columns: ["stockId"]
            isOneToOne: false
            referencedRelation: "stock_info"
            referencedColumns: ["id"]
          }
        ]
      }
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      buy_stock: {
        Args: {
          user_id: string
          stock_id: number
        }
        Returns: undefined
      }
      resolve_price_diff: {
        Args: {
          user_id: string
          price_diff: number
        }
        Returns: undefined
      }
      "sell_stock(depricated)": {
        Args: {
          user_id: string
          stock_id: number
          order_price: number
        }
        Returns: undefined
      }
      update_balance: {
        Args: {
          user_id: string
          price_delta: number
        }
        Returns: undefined
      }
    }
    Enums: {
      [_ in never]: never
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}

export type Tables<
  PublicTableNameOrOptions extends
    | keyof (Database["public"]["Tables"] & Database["public"]["Views"])
    | { schema: keyof Database },
  TableName extends PublicTableNameOrOptions extends { schema: keyof Database }
    ? keyof (Database[PublicTableNameOrOptions["schema"]]["Tables"] &
        Database[PublicTableNameOrOptions["schema"]]["Views"])
    : never = never
> = PublicTableNameOrOptions extends { schema: keyof Database }
  ? (Database[PublicTableNameOrOptions["schema"]]["Tables"] &
      Database[PublicTableNameOrOptions["schema"]]["Views"])[TableName] extends {
      Row: infer R
    }
    ? R
    : never
  : PublicTableNameOrOptions extends keyof (Database["public"]["Tables"] &
      Database["public"]["Views"])
  ? (Database["public"]["Tables"] &
      Database["public"]["Views"])[PublicTableNameOrOptions] extends {
      Row: infer R
    }
    ? R
    : never
  : never

export type TablesInsert<
  PublicTableNameOrOptions extends
    | keyof Database["public"]["Tables"]
    | { schema: keyof Database },
  TableName extends PublicTableNameOrOptions extends { schema: keyof Database }
    ? keyof Database[PublicTableNameOrOptions["schema"]]["Tables"]
    : never = never
> = PublicTableNameOrOptions extends { schema: keyof Database }
  ? Database[PublicTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Insert: infer I
    }
    ? I
    : never
  : PublicTableNameOrOptions extends keyof Database["public"]["Tables"]
  ? Database["public"]["Tables"][PublicTableNameOrOptions] extends {
      Insert: infer I
    }
    ? I
    : never
  : never

export type TablesUpdate<
  PublicTableNameOrOptions extends
    | keyof Database["public"]["Tables"]
    | { schema: keyof Database },
  TableName extends PublicTableNameOrOptions extends { schema: keyof Database }
    ? keyof Database[PublicTableNameOrOptions["schema"]]["Tables"]
    : never = never
> = PublicTableNameOrOptions extends { schema: keyof Database }
  ? Database[PublicTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Update: infer U
    }
    ? U
    : never
  : PublicTableNameOrOptions extends keyof Database["public"]["Tables"]
  ? Database["public"]["Tables"][PublicTableNameOrOptions] extends {
      Update: infer U
    }
    ? U
    : never
  : never

export type Enums<
  PublicEnumNameOrOptions extends
    | keyof Database["public"]["Enums"]
    | { schema: keyof Database },
  EnumName extends PublicEnumNameOrOptions extends { schema: keyof Database }
    ? keyof Database[PublicEnumNameOrOptions["schema"]]["Enums"]
    : never = never
> = PublicEnumNameOrOptions extends { schema: keyof Database }
  ? Database[PublicEnumNameOrOptions["schema"]]["Enums"][EnumName]
  : PublicEnumNameOrOptions extends keyof Database["public"]["Enums"]
  ? Database["public"]["Enums"][PublicEnumNameOrOptions]
  : never
