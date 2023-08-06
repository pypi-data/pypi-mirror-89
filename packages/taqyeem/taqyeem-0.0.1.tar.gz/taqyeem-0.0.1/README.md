#taqyeem
A python library for recording and reporting evaluation of ml models


## Usage
Here is a basic example of a k-fold cross validation experiment with two models:
``` python
from numpy.random import normal
from taqyeem import TaqKfoldCVExperiment

exp = TaqKfoldCVExperiment(name="simple_experiment", verbose=10)
exp.start_experiment()
for run_idx in range(5):
    for fold_idx in range(5):
        # train model >>>>>
        # eval model >>>>>
        alef_ap, alef_roc = normal(0.6, 0.1), normal(0.5, 0.1)
        geem_ap, geem_roc = normal(0.7, 0.1), normal(0.6, 0.1)
        exp.submit_cv_results("alef_model" , run_idx, fold_idx, metrics={"ap": alef_ap, "roc": alef_roc}, configs={"dataset": "nell"})
        exp.submit_cv_results("geem_model", run_idx, fold_idx, metrics={"ap": geem_ap, "roc": geem_roc}, configs={"dataset": "nell"})
exp.end_experiment()
```

The result logs should as follows:
```
[2020-12-20 23:26:21,359 - taqyeem - simple_experiment - DEBUG => experiment started
[2020-12-20 23:26:21,364 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: alef_model - config: {'dataset': 'nell', 'run': 0, 'fold': 0} - metrics: {'ap': 0.6307380380413475, 'roc': 0.6200565849091481} - hparams: None
[2020-12-20 23:26:21,367 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: geem_model - config: {'dataset': 'nell', 'run': 0, 'fold': 0} - metrics: {'ap': 0.8197700160418333, 'roc': 0.665177326089331} - hparams: None
[2020-12-20 23:26:21,370 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: alef_model - config: {'dataset': 'nell', 'run': 0, 'fold': 1} - metrics: {'ap': 0.6657005313702554, 'roc': 0.4337592673961494} - hparams: None
[2020-12-20 23:26:21,373 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: geem_model - config: {'dataset': 'nell', 'run': 0, 'fold': 1} - metrics: {'ap': 0.6628204587636084, 'roc': 0.4860280014973208} - hparams: None
[2020-12-20 23:26:21,377 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: alef_model - config: {'dataset': 'nell', 'run': 0, 'fold': 2} - metrics: {'ap': 0.6112029137775548, 'roc': 0.5621249085515367} - hparams: None
[2020-12-20 23:26:21,379 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: geem_model - config: {'dataset': 'nell', 'run': 0, 'fold': 2} - metrics: {'ap': 0.7491422137900099, 'roc': 0.5833850644802194} - hparams: None
[2020-12-20 23:26:21,382 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: alef_model - config: {'dataset': 'nell', 'run': 0, 'fold': 3} - metrics: {'ap': 0.6219454520741436, 'roc': 0.4851546212406319} - hparams: None
[2020-12-20 23:26:21,385 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: geem_model - config: {'dataset': 'nell', 'run': 0, 'fold': 3} - metrics: {'ap': 0.8589357951079609, 'roc': 0.5092078816902126} - hparams: None
[2020-12-20 23:26:21,388 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: alef_model - config: {'dataset': 'nell', 'run': 0, 'fold': 4} - metrics: {'ap': 0.448462324378197, 'roc': 0.4742821462096435} - hparams: None
[2020-12-20 23:26:21,390 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: geem_model - config: {'dataset': 'nell', 'run': 0, 'fold': 4} - metrics: {'ap': 0.8100394165153026, 'roc': 0.5666011711105432} - hparams: None
[2020-12-20 23:26:21,393 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: alef_model - config: {'dataset': 'nell', 'run': 1, 'fold': 0} - metrics: {'ap': 0.41521225983452736, 'roc': 0.40828552401974016} - hparams: None
[2020-12-20 23:26:21,396 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: geem_model - config: {'dataset': 'nell', 'run': 1, 'fold': 0} - metrics: {'ap': 0.626086510090878, 'roc': 0.4193996838453282} - hparams: None
[2020-12-20 23:26:21,399 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: alef_model - config: {'dataset': 'nell', 'run': 1, 'fold': 1} - metrics: {'ap': 0.7356639007940367, 'roc': 0.49847724174280444} - hparams: None
[2020-12-20 23:26:21,402 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: geem_model - config: {'dataset': 'nell', 'run': 1, 'fold': 1} - metrics: {'ap': 0.7538106272090022, 'roc': 0.6184834497076339} - hparams: None
[2020-12-20 23:26:21,405 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: alef_model - config: {'dataset': 'nell', 'run': 1, 'fold': 2} - metrics: {'ap': 0.44333351823756295, 'roc': 0.35422824118126484} - hparams: None
[2020-12-20 23:26:21,408 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: geem_model - config: {'dataset': 'nell', 'run': 1, 'fold': 2} - metrics: {'ap': 0.6787522103892222, 'roc': 0.6043439148468238} - hparams: None
[2020-12-20 23:26:21,410 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: alef_model - config: {'dataset': 'nell', 'run': 1, 'fold': 3} - metrics: {'ap': 0.5785525577703831, 'roc': 0.6214556949605816} - hparams: None
[2020-12-20 23:26:21,413 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: geem_model - config: {'dataset': 'nell', 'run': 1, 'fold': 3} - metrics: {'ap': 0.9161751389997288, 'roc': 0.6092723998074447} - hparams: None
[2020-12-20 23:26:21,416 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: alef_model - config: {'dataset': 'nell', 'run': 1, 'fold': 4} - metrics: {'ap': 0.5336898293887246, 'roc': 0.5487595569655326} - hparams: None
[2020-12-20 23:26:21,419 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: geem_model - config: {'dataset': 'nell', 'run': 1, 'fold': 4} - metrics: {'ap': 0.6703573163581318, 'roc': 0.6791856512683223} - hparams: None
[2020-12-20 23:26:21,422 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: alef_model - config: {'dataset': 'nell', 'run': 2, 'fold': 0} - metrics: {'ap': 0.4819250465433094, 'roc': 0.5198986273896734} - hparams: None
[2020-12-20 23:26:21,425 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: geem_model - config: {'dataset': 'nell', 'run': 2, 'fold': 0} - metrics: {'ap': 0.6752032930277466, 'roc': 0.6891711839291748} - hparams: None
[2020-12-20 23:26:21,428 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: alef_model - config: {'dataset': 'nell', 'run': 2, 'fold': 1} - metrics: {'ap': 0.703967227217891, 'roc': 0.5535185287463616} - hparams: None
[2020-12-20 23:26:21,430 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: geem_model - config: {'dataset': 'nell', 'run': 2, 'fold': 1} - metrics: {'ap': 0.7808922098382631, 'roc': 0.707498281629237} - hparams: None
[2020-12-20 23:26:21,433 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: alef_model - config: {'dataset': 'nell', 'run': 2, 'fold': 2} - metrics: {'ap': 0.5911109884653535, 'roc': 0.5094491664819923} - hparams: None
[2020-12-20 23:26:21,436 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: geem_model - config: {'dataset': 'nell', 'run': 2, 'fold': 2} - metrics: {'ap': 0.7050145013631216, 'roc': 0.6446320788073112} - hparams: None
[2020-12-20 23:26:21,439 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: alef_model - config: {'dataset': 'nell', 'run': 2, 'fold': 3} - metrics: {'ap': 0.5668275395703646, 'roc': 0.5376912918750675} - hparams: None
[2020-12-20 23:26:21,442 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: geem_model - config: {'dataset': 'nell', 'run': 2, 'fold': 3} - metrics: {'ap': 0.6873100024919846, 'roc': 0.7276881383935923} - hparams: None
[2020-12-20 23:26:21,445 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: alef_model - config: {'dataset': 'nell', 'run': 2, 'fold': 4} - metrics: {'ap': 0.6062974352824366, 'roc': 0.6527144810453613} - hparams: None
[2020-12-20 23:26:21,448 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: geem_model - config: {'dataset': 'nell', 'run': 2, 'fold': 4} - metrics: {'ap': 0.5767503869572663, 'roc': 0.566135953737278} - hparams: None
[2020-12-20 23:26:21,451 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: alef_model - config: {'dataset': 'nell', 'run': 3, 'fold': 0} - metrics: {'ap': 0.6598572959508485, 'roc': 0.5143990482689512} - hparams: None
[2020-12-20 23:26:21,453 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: geem_model - config: {'dataset': 'nell', 'run': 3, 'fold': 0} - metrics: {'ap': 0.8444893516894517, 'roc': 0.595292760282927} - hparams: None
[2020-12-20 23:26:21,456 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: alef_model - config: {'dataset': 'nell', 'run': 3, 'fold': 1} - metrics: {'ap': 0.6964382169891388, 'roc': 0.5173329195597023} - hparams: None
[2020-12-20 23:26:21,459 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: geem_model - config: {'dataset': 'nell', 'run': 3, 'fold': 1} - metrics: {'ap': 0.6309364657835208, 'roc': 0.6340587013812506} - hparams: None
[2020-12-20 23:26:21,462 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: alef_model - config: {'dataset': 'nell', 'run': 3, 'fold': 2} - metrics: {'ap': 0.6133024343079523, 'roc': 0.33994160289945896} - hparams: None
[2020-12-20 23:26:21,464 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: geem_model - config: {'dataset': 'nell', 'run': 3, 'fold': 2} - metrics: {'ap': 0.5994315017215507, 'roc': 0.4999702288663059} - hparams: None
[2020-12-20 23:26:21,468 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: alef_model - config: {'dataset': 'nell', 'run': 3, 'fold': 3} - metrics: {'ap': 0.5468526494385909, 'roc': 0.49720203920116346} - hparams: None
[2020-12-20 23:26:21,470 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: geem_model - config: {'dataset': 'nell', 'run': 3, 'fold': 3} - metrics: {'ap': 0.6253498650929994, 'roc': 0.7195480889231419} - hparams: None
[2020-12-20 23:26:21,473 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: alef_model - config: {'dataset': 'nell', 'run': 3, 'fold': 4} - metrics: {'ap': 0.5606799252065591, 'roc': 0.5616506006633917} - hparams: None
[2020-12-20 23:26:21,476 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: geem_model - config: {'dataset': 'nell', 'run': 3, 'fold': 4} - metrics: {'ap': 0.6847330864730742, 'roc': 0.447778529408855} - hparams: None
[2020-12-20 23:26:21,479 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: alef_model - config: {'dataset': 'nell', 'run': 4, 'fold': 0} - metrics: {'ap': 0.6928254981624833, 'roc': 0.3996950439603223} - hparams: None
[2020-12-20 23:26:21,482 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: geem_model - config: {'dataset': 'nell', 'run': 4, 'fold': 0} - metrics: {'ap': 0.7858109415834511, 'roc': 0.6533205918451581} - hparams: None
[2020-12-20 23:26:21,485 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: alef_model - config: {'dataset': 'nell', 'run': 4, 'fold': 1} - metrics: {'ap': 0.6601317326189595, 'roc': 0.46008155712909765} - hparams: None
[2020-12-20 23:26:21,488 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: geem_model - config: {'dataset': 'nell', 'run': 4, 'fold': 1} - metrics: {'ap': 0.8099845770974685, 'roc': 0.6692003967940223} - hparams: None
[2020-12-20 23:26:21,491 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: alef_model - config: {'dataset': 'nell', 'run': 4, 'fold': 2} - metrics: {'ap': 0.700203490619381, 'roc': 0.6351355048561005} - hparams: None
[2020-12-20 23:26:21,493 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: geem_model - config: {'dataset': 'nell', 'run': 4, 'fold': 2} - metrics: {'ap': 0.7977462100659283, 'roc': 0.5923727589409298} - hparams: None
[2020-12-20 23:26:21,496 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: alef_model - config: {'dataset': 'nell', 'run': 4, 'fold': 3} - metrics: {'ap': 0.4934593422402669, 'roc': 0.5298083133193713} - hparams: None
[2020-12-20 23:26:21,499 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: geem_model - config: {'dataset': 'nell', 'run': 4, 'fold': 3} - metrics: {'ap': 0.6406614311806266, 'roc': 0.40875431824540265} - hparams: None
[2020-12-20 23:26:21,502 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: alef_model - config: {'dataset': 'nell', 'run': 4, 'fold': 4} - metrics: {'ap': 0.43814546814403454, 'roc': 0.5418021857280578} - hparams: None
[2020-12-20 23:26:21,505 - taqyeem - simple_experiment - INFO =>  = RESULTS = model: geem_model - config: {'dataset': 'nell', 'run': 4, 'fold': 4} - metrics: {'ap': 0.6171232899807844, 'roc': 0.5265556193763228} - hparams: None
[2020-12-20 23:26:21,565 - taqyeem - simple_experiment - DEBUG => experiment ended - duration: 0:00:00.206357
[2020-12-20 23:26:21,566 - taqyeem - simple_experiment - DEBUG => Cross Validation Report:
+-------+------------+----------------+----------------+
|  run  |   model    |       ap       |      roc       |
+-------+------------+----------------+----------------+
|   0   | geem_model | 0.780 (±0.076) | 0.562 (±0.070) |
|   0   | alef_model | 0.596 (±0.085) | 0.515 (±0.075) |
+-------+------------+----------------+----------------+
|   1   | geem_model | 0.729 (±0.114) | 0.586 (±0.098) |
|   1   | alef_model | 0.541 (±0.127) | 0.486 (±0.107) |
+-------+------------+----------------+----------------+
|   2   | geem_model | 0.685 (±0.073) | 0.667 (±0.064) |
|   2   | alef_model | 0.590 (±0.080) | 0.555 (±0.057) |
+-------+------------+----------------+----------------+
|   3   | geem_model | 0.677 (±0.099) | 0.579 (±0.108) |
|   3   | alef_model | 0.615 (±0.064) | 0.486 (±0.085) |
+-------+------------+----------------+----------------+
|   4   | geem_model | 0.730 (±0.093) | 0.570 (±0.106) |
|   4   | alef_model | 0.597 (±0.122) | 0.513 (±0.089) |
+-------+------------+----------------+----------------+
|  avg  | geem_model | 0.720 (±0.041) | 0.593 (±0.042) |
|  avg  | alef_model | 0.588 (±0.028) | 0.511 (±0.028) |
+-------+------------+----------------+----------------+
```