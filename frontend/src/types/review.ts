export interface Review {
  id: number;
  user: number;
  user_name: string;
  product: number;
  rating: number;
  comment: string;
  created_at: string;
}

export interface CreateReviewPayload {
  product: number;
  rating: number;
  comment?: string;
}
