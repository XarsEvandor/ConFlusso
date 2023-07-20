using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace ConsoleSignalRServer
{
    public class Startup
    {
        public IConfiguration Configuration { get; }
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public void ConfigureServices(IServiceCollection services)
        {
            
            services.AddSignalR(
                    options => options.EnableDetailedErrors = true
                    
                ).AddJsonProtocol(
                    options => {options.PayloadSerializerOptions.PropertyNamingPolicy = null;}
                );

        }

        public void Configure(IApplicationBuilder app)
        {
            app.UseRouting();
            app.UseEndpoints(endpoints =>
            {
                endpoints.MapHub<CDataHub>("/DataHub");
            });
        }
    }
}
