import { SupabaseClient, Session } from '@supabase/supabase-js';

declare global {
	namespace App {
		interface Locals {
			supabase: SupabaseClient;
			/**
			 * A convenience helper so we can just call await getSession() instead
			 * ```
			 * const { data: { session } } = await supabase.auth.getSession()
			 * ```
			 */
			getSession(): Promise<Session | null>;
		}
		interface PageData {
			session: Session | null;
		}
		// interface Error {}
		// interface Platform {}
	}
}
