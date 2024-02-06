export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export interface Database {
  public: {
    Tables: {
      contributors: {
        Row: {
          description: string | null
          id: number
          image: string | null
          name: string
          role: string | null
        }
        Insert: {
          description?: string | null
          id?: number
          image?: string | null
          name: string
          role?: string | null
        }
        Update: {
          description?: string | null
          id?: number
          image?: string | null
          name?: string
          role?: string | null
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
      portfolio: {
        Row: {
          quantity: number
          stockId: number
          userId: string
        }
        Insert: {
          quantity?: number
          stockId?: number
          userId: string
        }
        Update: {
          quantity?: number
          stockId?: number
          userId?: string
        }
        Relationships: [
          {
            foreignKeyName: "portfolio_stockId_fkey"
            columns: ["stockId"]
            isOneToOne: false
            referencedRelation: "stockInfo"
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
          joined_at?: string
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
      stockInfo: {
        Row: {
          description: string | null
          id: number
          image: string | null
          name: string
          totalShares: number
        }
        Insert: {
          description?: string | null
          id?: number
          image?: string | null
          name: string
          totalShares?: number
        }
        Update: {
          description?: string | null
          id?: number
          image?: string | null
          name?: string
          totalShares?: number
        }
        Relationships: []
      }
      stockPrices: {
        Row: {
          stockId: number
          stockPrice: number
        }
        Insert: {
          stockId?: number
          stockPrice?: number
        }
        Update: {
          stockId?: number
          stockPrice?: number
        }
        Relationships: [
          {
            foreignKeyName: "stockPrices_stockId_fkey"
            columns: ["stockId"]
            isOneToOne: true
            referencedRelation: "stockInfo"
            referencedColumns: ["id"]
          }
        ]
      }
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      [_ in never]: never
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
