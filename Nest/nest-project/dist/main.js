"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const core_1 = require("@nestjs/core");
const path_1 = require("path");
const app_module_1 = require("./app.module");
async function bootstrap() {
    const app = await core_1.NestFactory.create(app_module_1.AppModule);
    app.useStaticAssets(path_1.resolve('./src/public'));
    app.useStaticAssets(path_1.resolve('./images'));
    app.useStaticAssets(path_1.resolve('./src/public/css'));
    app.useStaticAssets(path_1.resolve('./src/public/html'));
    app.setBaseViewsDir(path_1.resolve('./src/views'));
    app.setViewEngine('hbs');
    await app.listen(3000);
    if (module.hot) {
        module.hot.accept();
        module.hot.dispose(() => app.close());
    }
}
bootstrap();
//# sourceMappingURL=main.js.map