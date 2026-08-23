/**
 * SecureNova Project 4 Auth0 Post-Login Action.
 *
 * Configure a risk signal in app_metadata/user_metadata or from a trusted
 * upstream risk service. Never trust a user-supplied prompt as the risk signal.
 *
 * Example: deny login when event.user.app_metadata.ai_risk === "high".
 */
exports.onExecutePostLogin = async (event, api) => {
  const risk = event.user.app_metadata?.ai_risk;

  if (risk === "high") {
    api.access.deny("access_denied", "Login blocked by SecureNova risk policy.");
    return;
  }

  // Optional non-sensitive claim for downstream audit correlation.
  api.idToken.setCustomClaim("https://securenova.example/agent_id", event.user.user_id);
};
