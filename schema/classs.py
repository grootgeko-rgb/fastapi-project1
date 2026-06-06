from pydantic import BaseModel, Field, field_validator

class CustomerIntelligenceRequest(BaseModel):
    customer_id: str = Field(
        ...,
        min_length=1,
        pattern=r"\S",               # Rejects strings that are all whitespace
        description="The unique alphanumeric identifier of the customer in the database."
    )

    customer_review: str = Field(
        ...,
        min_length=5,
        max_length=1000,
        description="The live text review from the customer to be analyzed for sentiment."
    )

    @field_validator("customer_id", "customer_review")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("Field must not be empty or whitespace-only")
        return stripped


class CustomerIntelligenceResponse(BaseModel):
    """
    Production-grade response schema defining a strict output contract 
    for churn probabilities and textual sentiment evaluation.
    """
    customer_id: str = Field(
        ..., 
        description="The unique identifier of the analyzed customer."
    )
    
    # Tabular Churn Model Outputs
    churn_probability: float = Field(
        ..., 
        ge=0.0, 
        le=1.0, 
        description="The statistical probability of customer churn, bounded between 0.0 and 1.0." 
    )
    churn_risk_label: str = Field(
        ..., 
        description="Human-readable risk tier derived from the probability (e.g., Low, Medium, High)."
    )
    
    # Text Sentiment Model Outputs
    sentiment_score: float = Field(
        ..., 
        ge=-1.0, 
        le=1.0, 
        description="The raw compound sentiment score from VADER, ranging from -1.0 (negative) to 1.0 (positive)." 
    )
    sentiment_label: str = Field(
        ..., 
        description="The final categorized classification of the review text (Positive, Neutral, Negative)." )